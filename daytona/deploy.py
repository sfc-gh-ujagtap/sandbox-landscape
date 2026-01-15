"""
Daytona deployment script for Streamlit app.
Uses Daytona SDK to run Streamlit in a secure sandbox environment.
See: https://www.daytona.io/docs/
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from daytona import Daytona, DaytonaConfig, CreateSandboxFromImageParams

# Load environment variables from .env file
load_dotenv()

# Get the project root (parent of this file's directory)
project_root = Path(__file__).parent.parent

# Initialize Daytona client
# Set DAYTONA_API_KEY in .env file or as environment variable
config = DaytonaConfig(api_key=os.environ.get("DAYTONA_API_KEY"))
daytona = Daytona(config)

def deploy():
    """Deploy Streamlit app to Daytona sandbox."""
    print("🏎️ Creating Daytona Sandbox...")
    
    # Get Snowflake credentials from environment
    sf_account = os.environ.get("SNOWFLAKE_ACCOUNT", "")
    sf_user = os.environ.get("SNOWFLAKE_USER", "")
    sf_password = os.environ.get("SNOWFLAKE_PASSWORD", "")
    sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    
    # Create a public sandbox with environment variables
    params = CreateSandboxFromImageParams(
        image="daytonaio/sandbox:latest",
        public=True,
        env_vars={
            "SNOWFLAKE_ACCOUNT": sf_account,
            "SNOWFLAKE_USER": sf_user,
            "SNOWFLAKE_PASSWORD": sf_password,
            "SNOWFLAKE_WAREHOUSE": sf_warehouse
        }
    )
    
    sandbox = daytona.create(params)
    
    print(f"✅ Sandbox created: {sandbox.id}")
    
    # Upload the app files from project root
    sandbox.fs.upload_file(str(project_root / "app.py"), "app.py")
    sandbox.fs.upload_file(str(project_root / "requirements.txt"), "requirements.txt")
    
    print("📦 Installing dependencies...")
    
    # Install dependencies using shell command
    response = sandbox.process.exec("pip install -r requirements.txt", timeout=300)
    if response.exit_code != 0:
        print(f"❌ Error installing dependencies: {response.result}")
        return
    
    print("✅ Dependencies installed!")
    print("🚀 Starting Streamlit server...")
    
    # Run Streamlit in background (use python3 -m to ensure it's in PATH)
    # CORS and XSRF protection disabled to allow Daytona proxy to forward requests
    sandbox.process.exec(
        "python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false > /tmp/streamlit.log 2>&1 &",
        timeout=10
    )
    
    # Wait for server to start
    time.sleep(5)
    
    # Get the preview URL for the app
    preview = sandbox.get_preview_link(8501)
    
    print(f"📊 Streamlit app is running!")
    print(f"🔗 Access your app at: {preview.url}")
    
    return sandbox

if __name__ == "__main__":
    deploy()
