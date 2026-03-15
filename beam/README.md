# Beam.cloud Streamlit Deployment

Deploy the TPC-H Sales Dashboard to Beam.cloud using Pods.

## Files

| File | Description |
|------|-------------|
| `streamlit_app.py` | Streamlit TPC-H dashboard (connects to Snowflake) |
| `deploy.py` | Deployment script using Beam Pods |

## Prerequisites

Create Beam secrets for Snowflake credentials:

```bash
beam secret create SNOWFLAKE_ACCOUNT "your-account"
beam secret create SNOWFLAKE_USER "your-user"
beam secret create SNOWFLAKE_PAT "your-pat-token"
beam secret create SNOWFLAKE_WAREHOUSE "COMPUTE_WH"
```

## Deploy

```bash
python deploy.py
```

## How It Works

The deployment uses Beam Pods (long-running containers) to host the Streamlit app:

```python
pod = Pod(
    name="tpch-dashboard",
    image=Image(python_version="python3.11").add_python_packages([
        "streamlit", "pandas", "plotly", "snowflake-connector-python",
    ]),
    ports=[8501],
    entrypoint=["streamlit", "run", "streamlit_app.py", "--server.port=8501"],
    secrets=["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_PAT", "SNOWFLAKE_WAREHOUSE"],
)
```

## More Beam Examples

For comprehensive Beam.cloud examples (endpoints, task queues, functions, sandboxes, ML, etc.), see the [beam-examples](https://github.com/sfc-gh-ujagtap/beam-examples) repository.
