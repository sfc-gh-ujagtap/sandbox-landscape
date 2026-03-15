"""Beam.cloud deployment script for Streamlit and Next.js dashboards."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from beam import Image, Pod

load_dotenv(Path(__file__).parent.parent / ".env")


def deploy_streamlit():
    """Deploy Streamlit TPC-H dashboard to Beam.cloud."""
    print("🚀 Creating Beam.cloud Pod for Streamlit app...")
    sf_account = os.environ.get("SNOWFLAKE_ACCOUNT", "")
    sf_user = os.environ.get("SNOWFLAKE_USER", "")
    sf_password = os.environ.get("SNOWFLAKE_PASSWORD", "")
    sf_pat = os.environ.get("SNOWFLAKE_PAT", "")
    sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")

    streamlit_server = Pod(
        name="tpch-sales-dashboard-streamlit",
        image=Image(python_version="python3.11").add_python_packages([
            "streamlit",
            "pandas",
            "plotly",
            "snowflake-connector-python",
        ]),
        ports=[8501],
        cpu=2,
        memory=2048,
        entrypoint=["streamlit", "run", "streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"],
        env={
            "SNOWFLAKE_ACCOUNT": sf_account,
            "SNOWFLAKE_USER": sf_user,
            "SNOWFLAKE_PASSWORD": sf_password,
            "SNOWFLAKE_PAT": sf_pat,
            "SNOWFLAKE_WAREHOUSE": sf_warehouse,
        },
    )

    res = streamlit_server.create()
    print(f"✅ Streamlit Pod created successfully")
    print(f"📊 App running at: {res.url}")
    return res


def deploy_nextjs():
    """Deploy Next.js TPC-H dashboard to Beam.cloud."""
    print("🚀 Creating Beam.cloud Pod for Next.js app...")
    sf_account = os.environ.get("SNOWFLAKE_ACCOUNT", "")
    sf_user = os.environ.get("SNOWFLAKE_USER", "")
    sf_pat = os.environ.get("SNOWFLAKE_PAT", "")
    sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")

    nextjs_server = Pod(
        name="tpch-sales-dashboard-nextjs",
        image=Image(
            base_image="node:20-alpine",
            commands=[
                "npm install -g npm@latest",
            ],
        ),
        ports=[3000],
        cpu=2,
        memory=4096,
        entrypoint=["sh", "-c", "cd /mnt/code/nextjs-dashboard && npm install && npm run build && npm start"],
        env={
            "SNOWFLAKE_ACCOUNT": sf_account,
            "SNOWFLAKE_USER": sf_user,
            "SNOWFLAKE_PAT": sf_pat,
            "SNOWFLAKE_WAREHOUSE": sf_warehouse,
        },
    )

    res = nextjs_server.create()
    print(f"✅ Next.js Pod created successfully")
    print(f"📊 App running at: {res.url}")
    return res


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy.py [streamlit|nextjs|both]")
        print("  streamlit - Deploy Streamlit dashboard")
        print("  nextjs    - Deploy Next.js dashboard")
        print("  both      - Deploy both dashboards")
        sys.exit(1)
    
    target = sys.argv[1].lower()
    if target == "streamlit":
        deploy_streamlit()
    elif target == "nextjs":
        deploy_nextjs()
    elif target == "both":
        deploy_streamlit()
        deploy_nextjs()
    else:
        print(f"Unknown target: {target}")
        print("Use 'streamlit', 'nextjs', or 'both'")
        sys.exit(1)
