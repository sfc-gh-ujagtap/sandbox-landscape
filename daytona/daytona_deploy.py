"""
Daytona deployment script for Streamlit app.
Uses Daytona SDK to run Streamlit in a secure sandbox environment.
See: https://www.daytona.io/docs/
"""

import os
import time
from dotenv import load_dotenv
from daytona import Daytona, DaytonaConfig, CreateSandboxFromImageParams

# Load environment variables from .env file
load_dotenv()

# Initialize Daytona client
# Set DAYTONA_API_KEY in .env file or as environment variable
config = DaytonaConfig(api_key=os.environ.get("DAYTONA_API_KEY"))
daytona = Daytona(config)

def deploy():
    """Deploy Streamlit app to Daytona sandbox."""
    print("🏎️ Creating Daytona Sandbox...")
    
    # Create a public sandbox so the preview URL is accessible
    params = CreateSandboxFromImageParams(
        image="daytonaio/sandbox:latest",
        public=True
    )
    
    sandbox = daytona.create(params)
    
    print(f"✅ Sandbox created: {sandbox.id}")
    
    # Upload the app files
    sandbox.fs.upload_file("app.py", "app.py")
    sandbox.fs.upload_file("requirements.txt", "requirements.txt")
    
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
