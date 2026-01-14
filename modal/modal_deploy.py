"""
Simple Modal deployment script for Streamlit app with mock data.
This deploys a clean sales dashboard with generated mock data.
"""

import modal
from pathlib import Path

# Create a Modal app
app = modal.App("streamlit-sales-dashboard")

# Get the local path to app.py
local_path = Path(__file__).parent

# Define the image with required dependencies and include app.py
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements(local_path / "requirements.txt")
    .add_local_file(local_path / "app.py", "/root/app.py")
)

@app.function(
    image=image,
    timeout=3600
)
@modal.web_server(8501, startup_timeout=60)
def run_streamlit():
    import subprocess
    subprocess.Popen([
        "streamlit", "run", "/root/app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ])

@app.local_entrypoint()
def main():
    print("🚀 Deploying Sales Dashboard to Modal...")
    print("📊 Your Streamlit app will be available at the provided URL")
    print("⚡ App is now running on Modal!")
