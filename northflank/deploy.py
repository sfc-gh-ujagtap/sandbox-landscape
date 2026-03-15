"""Northflank deployment script for Streamlit TPC-H dashboard."""
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
project_root = Path(__file__).parent.parent
northflank_dir = Path(__file__).parent

def deploy():
    print("🏔️ Northflank Deployment")
    shutil.copy(project_root / "app.py", northflank_dir / "app.py")
    shutil.copy(project_root / "requirements.txt", northflank_dir / "requirements.txt")
    print("📦 Files prepared")
    print("""
To deploy:
1. npm install -g @northflank/cli
2. northflank login
3. northflank create project --name streamlit-tpch
4. northflank create service --project streamlit-tpch --name dashboard --dockerfile ./Dockerfile --port 8501
5. Set env vars in dashboard: SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_WAREHOUSE
""")

if __name__ == "__main__":
    deploy()
