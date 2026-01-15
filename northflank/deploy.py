"""
Northflank deployment script for Streamlit app.
Uses Northflank API to deploy a containerized Streamlit application.
See: https://northflank.com/docs
"""

import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the project root (parent of this file's directory)
project_root = Path(__file__).parent.parent
northflank_dir = Path(__file__).parent

# Northflank configuration
PROJECT_ID = "streamlit-tpch"
SERVICE_NAME = "tpch-dashboard"


def check_cli_installed():
    """Check if Northflank CLI is installed."""
    try:
        result = subprocess.run(
            ["northflank", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def deploy_with_cli():
    """Deploy using Northflank CLI."""
    print("🚀 Deploying to Northflank...")
    
    # Get Snowflake credentials from environment
    sf_account = os.environ.get("SNOWFLAKE_ACCOUNT", "")
    sf_user = os.environ.get("SNOWFLAKE_USER", "")
    sf_password = os.environ.get("SNOWFLAKE_PASSWORD", "")
    sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    
    # Copy app.py and requirements.txt to northflank directory for Docker build
    import shutil
    shutil.copy(project_root / "app.py", northflank_dir / "app.py")
    shutil.copy(project_root / "requirements.txt", northflank_dir / "requirements.txt")
    
    print("📦 Files prepared for deployment")
    print(f"📁 Build context: {northflank_dir}")
    
    # Instructions for manual deployment
    print("\n" + "="*60)
    print("📋 NORTHFLANK DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    print("""
1. Install Northflank CLI (if not installed):
   npm install -g @northflank/cli

2. Login to Northflank:
   northflank login

3. Create a project (first time only):
   northflank create project --name streamlit-tpch

4. Deploy the service from this directory:
   cd northflank
   northflank create service \\
     --project streamlit-tpch \\
     --name tpch-dashboard \\
     --type deployment \\
     --dockerfile ./Dockerfile \\
     --port 8501

5. Set environment variables in Northflank dashboard:
   - SNOWFLAKE_ACCOUNT
   - SNOWFLAKE_USER
   - SNOWFLAKE_PASSWORD
   - SNOWFLAKE_WAREHOUSE

Or use the Northflank web UI at https://app.northflank.com
""")
    
    # Try to deploy if CLI is available and authenticated
    if check_cli_installed():
        print("\n✅ Northflank CLI detected!")
        print("Attempting automatic deployment...")
        
        try:
            # Check if logged in
            result = subprocess.run(
                ["northflank", "whoami"],
                capture_output=True,
                text=True,
                cwd=northflank_dir
            )
            
            if result.returncode == 0:
                print(f"👤 Logged in as: {result.stdout.strip()}")
                
                # Create project if it doesn't exist
                subprocess.run(
                    ["northflank", "create", "project", "--name", PROJECT_ID],
                    capture_output=True,
                    text=True
                )
                
                # Deploy the service
                deploy_result = subprocess.run(
                    [
                        "northflank", "create", "service",
                        "--project", PROJECT_ID,
                        "--name", SERVICE_NAME,
                        "--type", "deployment",
                        "--dockerfile", "./Dockerfile",
                        "--port", "8501"
                    ],
                    capture_output=True,
                    text=True,
                    cwd=northflank_dir
                )
                
                if deploy_result.returncode == 0:
                    print("✅ Service deployed successfully!")
                    print(deploy_result.stdout)
                else:
                    print(f"⚠️ Deployment output: {deploy_result.stderr}")
                    
            else:
                print("⚠️ Not logged in. Run 'northflank login' first.")
                
        except Exception as e:
            print(f"⚠️ CLI deployment failed: {e}")
            print("Please follow the manual instructions above.")
    else:
        print("\n⚠️ Northflank CLI not found.")
        print("Install with: npm install -g @northflank/cli")
    
    return True


def deploy():
    """Main deployment function."""
    print("🏔️ Northflank Deployment")
    print("="*40)
    
    # Check for API token
    api_token = os.environ.get("NORTHFLANK_API_TOKEN")
    if api_token:
        print("✅ API token found")
    else:
        print("ℹ️ No API token set (NORTHFLANK_API_TOKEN)")
    
    return deploy_with_cli()


if __name__ == "__main__":
    deploy()
