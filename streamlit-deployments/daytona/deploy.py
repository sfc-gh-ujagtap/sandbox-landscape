"""Daytona deployment script for Streamlit TPC-H dashboard."""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from daytona import Daytona, DaytonaConfig, CreateSandboxFromImageParams

load_dotenv()
project_root = Path(__file__).parent.parent
config = DaytonaConfig(api_key=os.environ.get("DAYTONA_API_KEY"))
daytona = Daytona(config)

def deploy():
    print("🏎️ Creating Daytona Sandbox...")
    sf_account = os.environ.get("SNOWFLAKE_ACCOUNT", "")
    sf_user = os.environ.get("SNOWFLAKE_USER", "")
    sf_password = os.environ.get("SNOWFLAKE_PASSWORD", "")
    sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    
    params = CreateSandboxFromImageParams(
        image="daytonaio/sandbox:latest", public=True,
        env_vars={"SNOWFLAKE_ACCOUNT": sf_account, "SNOWFLAKE_USER": sf_user, "SNOWFLAKE_PASSWORD": sf_password, "SNOWFLAKE_WAREHOUSE": sf_warehouse}
    )
    sandbox = daytona.create(params)
    print(f"✅ Sandbox created: {sandbox.id}")
    
    sandbox.fs.upload_file(str(project_root / "app.py"), "app.py")
    sandbox.fs.upload_file(str(project_root / "requirements.txt"), "requirements.txt")
    
    print("📦 Installing dependencies...")
    response = sandbox.process.exec("pip install -r requirements.txt", timeout=300)
    if response.exit_code != 0:
        print(f"❌ Error: {response.result}")
        return
    
    print("🚀 Starting Streamlit...")
    sandbox.process.exec("python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > /tmp/streamlit.log 2>&1 &", timeout=10)
    time.sleep(5)
    
    preview = sandbox.get_preview_link(8501)
    print(f"📊 App running at: {preview.url}")
    return sandbox

if __name__ == "__main__":
    deploy()
