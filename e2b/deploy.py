"""
E2B deployment script for Streamlit app.
Uses E2B SDK to run Streamlit in a secure sandbox environment.
See: https://e2b.dev/docs
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Load environment variables from .env file
load_dotenv()

# Get the project root (parent of this file's directory)
project_root = Path(__file__).parent.parent


def deploy():
    """Deploy Streamlit app to E2B sandbox."""
    print("🚀 Creating E2B Sandbox...")
    
    # Create sandbox - requires E2B_API_KEY environment variable
    # Set E2B_API_KEY in .env file or as environment variable
    sandbox = Sandbox()
    
    print(f"✅ Sandbox created: {sandbox.sandbox_id}")
    
    # Read app files from project root
    app_content = (project_root / "app.py").read_text()
    requirements_content = (project_root / "requirements.txt").read_text()
    
    # Write files to sandbox
    sandbox.files.write("/home/user/app.py", app_content)
    sandbox.files.write("/home/user/requirements.txt", requirements_content)
    
    print("📦 Installing dependencies...")
    
    # Install dependencies
    result = sandbox.commands.run("pip install -r /home/user/requirements.txt", timeout=300)
    if result.exit_code != 0:
        print(f"❌ Error installing dependencies: {result.stderr}")
        return None
    
    print("✅ Dependencies installed!")
    print("🚀 Starting Streamlit server...")
    
    # Get Snowflake credentials from environment
    sf_account = os.environ.get("SNOWFLAKE_ACCOUNT", "")
    sf_user = os.environ.get("SNOWFLAKE_USER", "")
    sf_password = os.environ.get("SNOWFLAKE_PASSWORD", "")
    sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    
    # Run Streamlit in background with Snowflake env vars
    sandbox.commands.run(
        f"SNOWFLAKE_ACCOUNT='{sf_account}' "
        f"SNOWFLAKE_USER='{sf_user}' "
        f"SNOWFLAKE_PASSWORD='{sf_password}' "
        f"SNOWFLAKE_WAREHOUSE='{sf_warehouse}' "
        "nohup streamlit run /home/user/app.py "
        "--server.port 8501 "
        "--server.address 0.0.0.0 "
        "--server.headless true "
        "--server.enableCORS false "
        "--server.enableXsrfProtection false "
        "> /tmp/streamlit.log 2>&1 &",
        background=True
    )
    
    # Wait for server to start
    time.sleep(5)
    
    # Get the host URL
    host = sandbox.get_host(8501)
    url = f"https://{host}"
    
    print(f"📊 Streamlit app is running!")
    print(f"🔗 Access your app at: {url}")
    print(f"⏱️  Sandbox will stay alive for the default timeout (check E2B docs for limits)")
    print(f"💡 To keep it running longer, use sandbox.set_timeout()")
    
    return sandbox


if __name__ == "__main__":
    deploy()
