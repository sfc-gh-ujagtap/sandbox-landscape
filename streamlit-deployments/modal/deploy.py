"""Modal deployment script for Streamlit TPC-H dashboard."""
import os
import modal
from pathlib import Path

app = modal.App("streamlit-tpch-dashboard")
project_root = Path(__file__).parent.parent

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements(project_root / "requirements.txt")
    .pip_install("modal==1.3.0")
    .add_local_file(project_root / "app.py", "/root/app.py")
)

@app.function(image=image, timeout=3600, secrets=[modal.Secret.from_name("snowflake-credentials")])
@modal.web_server(8501, startup_timeout=60)
def run_streamlit():
    import subprocess
    subprocess.Popen(["streamlit", "run", "/root/app.py", "--server.port", "8501", "--server.address", "0.0.0.0", "--server.headless", "true"])

@app.local_entrypoint()
def main():
    print("🚀 Deploying to Modal...")
