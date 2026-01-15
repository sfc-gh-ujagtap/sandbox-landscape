# 📊 Streamlit Deployments

A Streamlit TPC-H sales dashboard with deployment options for Modal, Daytona, E2B, and Northflank.

## 📁 Project Structure

```
streamlit-deployments/
├── app.py                    # Shared Streamlit dashboard (Snowflake TPC-H)
├── requirements.txt          # App dependencies
├── modal/                    # Modal.com deployment
│   ├── deploy.py            # Modal deployment script
│   └── requirements.txt     # Modal-specific dependencies
├── daytona/                  # Daytona.io deployment
│   ├── deploy.py            # Daytona deployment script
│   └── requirements.txt     # Daytona-specific dependencies
├── e2b/                      # E2B.dev deployment
│   ├── deploy.py            # E2B deployment script
│   └── requirements.txt     # E2B-specific dependencies
├── northflank/               # Northflank.com deployment
│   ├── deploy.py            # Northflank deployment script
│   ├── Dockerfile           # Container definition
│   └── requirements.txt     # Northflank-specific dependencies
└── README.md
```

## 🚀 Local Development

```bash
pip install -r requirements.txt
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_USER="your-user"
export SNOWFLAKE_PASSWORD="your-password"
streamlit run app.py
```

## 🚀 Deployment Options

### Modal Deployment

[Modal](https://modal.com) provides serverless cloud functions with auto-scaling.

```bash
pip install -r modal/requirements.txt
modal setup  # First time only
modal secret create snowflake-credentials \
  SNOWFLAKE_ACCOUNT="your-account" \
  SNOWFLAKE_USER="your-user" \
  SNOWFLAKE_PASSWORD="your-password"
modal deploy modal/deploy.py
```

### Daytona Deployment

[Daytona](https://daytona.io) provides secure sandbox environments.

```bash
pip install -r daytona/requirements.txt
export DAYTONA_API_KEY="your-api-key"
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_USER="your-user"
export SNOWFLAKE_PASSWORD="your-password"
python daytona/deploy.py
```

### E2B Deployment

[E2B](https://e2b.dev) provides AI sandboxes for secure code execution.

```bash
pip install -r e2b/requirements.txt
export E2B_API_KEY="your-api-key"
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_USER="your-user"
export SNOWFLAKE_PASSWORD="your-password"
python e2b/deploy.py
```

### Northflank Deployment

[Northflank](https://northflank.com) provides container deployment on managed or your own cloud.

```bash
# Install Northflank CLI
npm install -g @northflank/cli

# Login to Northflank
northflank login

# Deploy
cd northflank
python deploy.py
```

Or deploy manually via CLI:

```bash
cd northflank
northflank create project --name streamlit-tpch
northflank create service \
  --project streamlit-tpch \
  --name tpch-dashboard \
  --type deployment \
  --dockerfile ./Dockerfile \
  --port 8501
```

Then set environment variables in the Northflank dashboard:
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_WAREHOUSE`

## 📊 Dashboard Features

- **Key Metrics**: Total revenue, orders, customers, and average order value
- **Revenue Trend**: Line chart showing monthly revenue over time
- **Top Nations**: Bar chart of revenue by nation (TPC-H data)
- **Order Priorities**: Pie chart of order distribution
- **Top Parts**: Horizontal bar chart of top selling parts
- **Data Tables**: Recent orders with customer details
- **Interactive Filter**: Year selector for time-based analysis
