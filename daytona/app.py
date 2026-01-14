import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Daytona Dashboard",
    page_icon="🏎️",
    layout="wide"
)

# Title and description
st.title("🏎️ Daytona Dashboard")
st.markdown("A dashboard ready for Snowflake data integration")

# Generate mock data (replace with Snowflake query)
@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    
    # Generate dates for the last 30 days
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    
    # Generate mock sales data
    sales_data = {
        'Date': dates,
        'Sales': np.random.randint(1000, 5000, 30),
        'Orders': np.random.randint(50, 200, 30),
        'Customers': np.random.randint(30, 150, 30)
    }
    
    # Generate product data
    products = ['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones']
    product_data = {
        'Product': products,
        'Revenue': np.random.randint(10000, 50000, 5),
        'Units_Sold': np.random.randint(100, 500, 5)
    }
    
    return pd.DataFrame(sales_data), pd.DataFrame(product_data)

# Load data
sales_df, products_df = generate_mock_data()

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${sales_df['Sales'].sum():,}")

with col2:
    st.metric("Total Orders", f"{sales_df['Orders'].sum():,}")

with col3:
    st.metric("Total Customers", f"{sales_df['Customers'].sum():,}")

with col4:
    avg_order = sales_df['Sales'].sum() / sales_df['Orders'].sum()
    st.metric("Avg Order Value", f"${avg_order:.2f}")

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Daily Sales Trend")
    fig1 = px.line(sales_df, x='Date', y='Sales', 
                   title='Sales Over Time',
                   markers=True)
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🛍️ Product Revenue")
    fig2 = px.bar(products_df, x='Product', y='Revenue',
                  title='Revenue by Product',
                  color='Revenue',
                  color_continuous_scale='Blues')
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Data tables
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Recent Sales Data")
    st.dataframe(sales_df.tail(10), use_container_width=True, hide_index=True)

with col2:
    st.subheader("🏆 Product Performance")
    st.dataframe(products_df, use_container_width=True, hide_index=True)

# Interactive filter
st.divider()
st.subheader("🔍 Interactive Analysis")

selected_days = st.slider("Select number of days to analyze", 7, 30, 14)
filtered_data = sales_df.tail(selected_days)

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Sales Summary (Last {selected_days} days):**")
    st.write(f"- Total Sales: ${filtered_data['Sales'].sum():,}")
    st.write(f"- Average Daily Sales: ${filtered_data['Sales'].mean():.2f}")
    st.write(f"- Best Day: ${filtered_data['Sales'].max():,}")

with col2:
    fig3 = px.area(filtered_data, x='Date', y='Sales',
                   title=f'Sales Trend (Last {selected_days} days)')
    st.plotly_chart(fig3, use_container_width=True)

st.success("✅ Dashboard loaded successfully!")
