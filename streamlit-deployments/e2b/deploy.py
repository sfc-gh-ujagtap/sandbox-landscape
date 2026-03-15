"""E2B deployment script for Streamlit TPC-H dashboard."""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()
project_root = Path(__file__).parent.parent

def deploy():
    print("🚀 Creating E2B Sandbox...")
    sandbox = Sandbox()
    print(f"✅ Sandbox created: {sandbox.sandbox_id}")
    
    app_content = (project_root / "app.py").read_text()
    requirements_content = (project_root / "requirements.txt").read_text()
    sandbox.files.write("/home/user/app.py", app_content)
    sandbox.files.write("/home/user/requirements.txt", requirements_content)
    
    print("📦 Installing dependencies...")
    result = sandbox.commands.run("pip install -r /home/user/requirements.txt", timeout=300)
    if result.exit_code != 0:
        print(f"❌ Error: {result.stderr}")
        return None
    
    print("🚀 Starting Streamlit...")
    sf_account = os.environ.get("SNOWFLAKE_ACCOUNT", "")
    sf_user = os.environ.get("SNOWFLAKE_USER", "")
    sf_password = os.environ.get("SNOWFLAKE_PASSWORD", "")
    sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    
    sandbox.commands.run(
        f"SNOWFLAKE_ACCOUNT='{sf_account}' SNOWFLAKE_USER='{sf_user}' SNOWFLAKE_PASSWORD='{sf_password}' SNOWFLAKE_WAREHOUSE='{sf_warehouse}' "
        "nohup streamlit run /home/user/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > /tmp/streamlit.log 2>&1 &",
        background=True
    )
    time.sleep(5)
    
    host = sandbox.get_host(8501)
    print(f"📊 App running at: https://{host}")
    return sandbox

if __name__ == "__main__":
    deploy()
