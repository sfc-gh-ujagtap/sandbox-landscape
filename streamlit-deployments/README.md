# Streamlit TPC-H Dashboard Deployments

Deploy to Modal, E2B, Daytona, or Northflank.

## Deploy Commands

### E2B
```bash
export E2B_API_KEY="your-key" SNOWFLAKE_ACCOUNT="PM" SNOWFLAKE_USER="ujagtap" SNOWFLAKE_PASSWORD="your-pat"
python e2b/deploy.py
```

### Modal
```bash
modal deploy modal/deploy.py
```

### Daytona
```bash
export DAYTONA_API_KEY="your-key" SNOWFLAKE_ACCOUNT="PM" SNOWFLAKE_USER="ujagtap" SNOWFLAKE_PASSWORD="your-pat"
python daytona/deploy.py
```

### Northflank
```bash
northflank login
cd northflank && python deploy.py
```
