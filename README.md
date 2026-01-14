# 📊 Streamlit Deployments

A collection of Streamlit dashboard deployments using different cloud platforms.

## 📁 Project Structure

```
streamlit-deployments/
├── modal/                    # Modal.com deployment
│   ├── app.py               # Streamlit sales dashboard
│   ├── modal_deploy.py      # Modal deployment script
│   └── requirements.txt     # Python dependencies
├── daytona/                  # Daytona.io deployment
│   ├── app.py               # Streamlit dashboard (Snowflake-ready)
│   ├── daytona_deploy.py    # Daytona deployment script
│   └── requirements.txt     # Python dependencies
└── README.md                # This file
```

## 🚀 Deployment Options

### Modal Deployment

[Modal](https://modal.com) provides serverless cloud functions with auto-scaling.

```bash
cd modal
pip install -r requirements.txt
modal setup  # First time only
modal deploy modal_deploy.py
```

**Features:**
- Automatic scaling based on traffic
- Built-in SSL and CDN
- No server management required

### Daytona Deployment

[Daytona](https://daytona.io) provides secure sandbox environments.

```bash
cd daytona
pip install -r requirements.txt
export DAYTONA_API_KEY="your-api-key"
python daytona_deploy.py
```

**Features:**
- Secure sandbox execution
- Snowflake integration ready
- Preview URLs for sharing

## 📊 Dashboard Features

Both dashboards include:
- **Key Metrics**: Total sales, orders, customers, and average order value
- **Sales Trend**: Line chart showing daily sales over time
- **Product Revenue**: Bar chart of revenue by product
- **Data Tables**: Recent sales data and product performance
- **Interactive Filter**: Slider to analyze different time periods

## 🛠️ Local Development

Run either dashboard locally:

```bash
cd modal  # or cd daytona
pip install -r requirements.txt
streamlit run app.py
```

## 📈 Sample Data

Both dashboards use generated mock data:
- 30 days of sales, orders, and customer data
- 5 products with revenue and units sold
- Realistic business metrics

## 🔧 Customization

1. **Modify Data**: Edit the `generate_mock_data()` function
2. **Add Charts**: Use Plotly Express for new visualizations
3. **Change Layout**: Adjust `st.columns()` and component placement
4. **Add Interactivity**: Include more Streamlit widgets
