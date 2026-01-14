# 📊 Streamlit Deployments

A Streamlit sales dashboard with deployment options for Modal and Daytona.

## 📁 Project Structure

```
streamlit-deployments/
├── app.py                    # Shared Streamlit dashboard
├── requirements.txt          # App dependencies
├── modal/                    # Modal.com deployment
│   ├── deploy.py            # Modal deployment script
│   └── requirements.txt     # Modal-specific dependencies
├── daytona/                  # Daytona.io deployment
│   ├── deploy.py            # Daytona deployment script
│   └── requirements.txt     # Daytona-specific dependencies
└── README.md
```

## 🚀 Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🚀 Deployment Options

### Modal Deployment

[Modal](https://modal.com) provides serverless cloud functions with auto-scaling.

```bash
pip install -r modal/requirements.txt
modal setup  # First time only
modal deploy modal/deploy.py
```

### Daytona Deployment

[Daytona](https://daytona.io) provides secure sandbox environments.

```bash
pip install -r daytona/requirements.txt
export DAYTONA_API_KEY="your-api-key"
python daytona/deploy.py
```

## 📊 Dashboard Features

- **Key Metrics**: Total sales, orders, customers, and average order value
- **Sales Trend**: Line chart showing daily sales over time
- **Product Revenue**: Bar chart of revenue by product
- **Data Tables**: Recent sales data and product performance
- **Interactive Filter**: Slider to analyze different time periods
