import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(
    page_title="TPC-H Sales Dashboard",
    page_icon="❄️",
    layout="wide"
)

# Title and description
st.title("❄️ TPC-H Sales Dashboard")
st.markdown("Sales analytics powered by Snowflake TPC-H sample data")

# Snowflake connection using environment variables
@st.cache_resource
def get_snowflake_connection():
    import snowflake.connector
    return snowflake.connector.connect(
        account=os.environ.get("SNOWFLAKE_ACCOUNT"),
        user=os.environ.get("SNOWFLAKE_USER"),
        password=os.environ.get("SNOWFLAKE_PASSWORD"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database="SNOWFLAKE_SAMPLE_DATA",
        schema="TPCH_SF1"
    )

@st.cache_data(ttl=600)
def get_orders_summary():
    """Get orders summary by date."""
    conn = get_snowflake_connection()
    query = """
    SELECT 
        DATE_TRUNC('month', O_ORDERDATE) as ORDER_MONTH,
        COUNT(*) as ORDER_COUNT,
        SUM(O_TOTALPRICE) as TOTAL_REVENUE,
        COUNT(DISTINCT O_CUSTKEY) as UNIQUE_CUSTOMERS
    FROM ORDERS
    WHERE O_ORDERDATE >= '1995-01-01'
    GROUP BY DATE_TRUNC('month', O_ORDERDATE)
    ORDER BY ORDER_MONTH
    """
    return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_top_nations():
    """Get revenue by nation."""
    conn = get_snowflake_connection()
    query = """
    SELECT 
        N.N_NAME as NATION,
        SUM(O.O_TOTALPRICE) as TOTAL_REVENUE,
        COUNT(DISTINCT C.C_CUSTKEY) as CUSTOMER_COUNT
    FROM ORDERS O
    JOIN CUSTOMER C ON O.O_CUSTKEY = C.C_CUSTKEY
    JOIN NATION N ON C.C_NATIONKEY = N.N_NATIONKEY
    GROUP BY N.N_NAME
    ORDER BY TOTAL_REVENUE DESC
    LIMIT 10
    """
    return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_order_priorities():
    """Get order counts by priority."""
    conn = get_snowflake_connection()
    query = """
    SELECT 
        O_ORDERPRIORITY as PRIORITY,
        COUNT(*) as ORDER_COUNT,
        SUM(O_TOTALPRICE) as TOTAL_REVENUE
    FROM ORDERS
    GROUP BY O_ORDERPRIORITY
    ORDER BY ORDER_COUNT DESC
    """
    return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_top_parts():
    """Get top selling parts."""
    conn = get_snowflake_connection()
    query = """
    SELECT 
        P.P_NAME as PART_NAME,
        P.P_TYPE as PART_TYPE,
        SUM(L.L_QUANTITY) as TOTAL_QUANTITY,
        SUM(L.L_EXTENDEDPRICE) as TOTAL_REVENUE
    FROM LINEITEM L
    JOIN PART P ON L.L_PARTKEY = P.P_PARTKEY
    GROUP BY P.P_NAME, P.P_TYPE
    ORDER BY TOTAL_REVENUE DESC
    LIMIT 10
    """
    return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_recent_orders():
    """Get recent orders."""
    conn = get_snowflake_connection()
    query = """
    SELECT 
        O.O_ORDERKEY,
        O.O_ORDERDATE,
        C.C_NAME as CUSTOMER_NAME,
        O.O_TOTALPRICE,
        O.O_ORDERSTATUS,
        O.O_ORDERPRIORITY
    FROM ORDERS O
    JOIN CUSTOMER C ON O.O_CUSTKEY = C.C_CUSTKEY
    ORDER BY O.O_ORDERDATE DESC
    LIMIT 100
    """
    return pd.read_sql(query, conn)

# Check for Snowflake credentials
if not all([os.environ.get("SNOWFLAKE_ACCOUNT"), 
            os.environ.get("SNOWFLAKE_USER"), 
            os.environ.get("SNOWFLAKE_PASSWORD")]):
    st.error("⚠️ Snowflake credentials not configured!")
    st.markdown("""
    Please set the following environment variables:
    - `SNOWFLAKE_ACCOUNT` - Your Snowflake account identifier
    - `SNOWFLAKE_USER` - Your Snowflake username
    - `SNOWFLAKE_PASSWORD` - Your Snowflake password
    - `SNOWFLAKE_WAREHOUSE` (optional) - Warehouse name (defaults to COMPUTE_WH)
    """)
    st.stop()

# Load data
try:
    with st.spinner("Loading data from Snowflake..."):
        orders_df = get_orders_summary()
        nations_df = get_top_nations()
        priorities_df = get_order_priorities()
        parts_df = get_top_parts()
        recent_orders_df = get_recent_orders()
except Exception as e:
    st.error(f"❌ Error connecting to Snowflake: {e}")
    st.stop()

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = orders_df['TOTAL_REVENUE'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

with col2:
    total_orders = orders_df['ORDER_COUNT'].sum()
    st.metric("Total Orders", f"{total_orders:,}")

with col3:
    total_customers = nations_df['CUSTOMER_COUNT'].sum()
    st.metric("Total Customers", f"{total_customers:,}")

with col4:
    avg_order = total_revenue / total_orders if total_orders > 0 else 0
    st.metric("Avg Order Value", f"${avg_order:,.2f}")

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Revenue Trend")
    fig1 = px.line(orders_df, x='ORDER_MONTH', y='TOTAL_REVENUE',
                   title='Revenue Over Time',
                   markers=True)
    fig1.update_layout(height=400)
    fig1.update_xaxes(title="Month")
    fig1.update_yaxes(title="Revenue ($)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🌍 Revenue by Nation (Top 10)")
    fig2 = px.bar(nations_df, x='NATION', y='TOTAL_REVENUE',
                  title='Top 10 Nations by Revenue',
                  color='TOTAL_REVENUE',
                  color_continuous_scale='Blues')
    fig2.update_layout(height=400)
    fig2.update_xaxes(title="Nation")
    fig2.update_yaxes(title="Revenue ($)")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Orders by Priority")
    fig3 = px.pie(priorities_df, values='ORDER_COUNT', names='PRIORITY',
                  title='Order Distribution by Priority')
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🏆 Top Selling Parts")
    fig4 = px.bar(parts_df, x='TOTAL_REVENUE', y='PART_NAME',
                  orientation='h',
                  title='Top 10 Parts by Revenue',
                  color='TOTAL_REVENUE',
                  color_continuous_scale='Greens')
    fig4.update_layout(height=400)
    fig4.update_xaxes(title="Revenue ($)")
    fig4.update_yaxes(title="Part Name")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Data tables
st.subheader("📋 Recent Orders")
st.dataframe(
    recent_orders_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "O_ORDERKEY": "Order ID",
        "O_ORDERDATE": st.column_config.DateColumn("Order Date"),
        "CUSTOMER_NAME": "Customer",
        "O_TOTALPRICE": st.column_config.NumberColumn("Total Price", format="$%.2f"),
        "O_ORDERSTATUS": "Status",
        "O_ORDERPRIORITY": "Priority"
    }
)

# Interactive filter
st.divider()
st.subheader("🔍 Interactive Analysis")

# Year filter - convert to datetime if needed
orders_df['ORDER_MONTH'] = pd.to_datetime(orders_df['ORDER_MONTH'])
years = orders_df['ORDER_MONTH'].dt.year.unique()
selected_year = st.selectbox("Select Year", sorted(years, reverse=True))

filtered_data = orders_df[orders_df['ORDER_MONTH'].dt.year == selected_year]

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Summary for {selected_year}:**")
    st.write(f"- Total Revenue: ${filtered_data['TOTAL_REVENUE'].sum():,.0f}")
    st.write(f"- Total Orders: {filtered_data['ORDER_COUNT'].sum():,}")
    st.write(f"- Unique Customers: {filtered_data['UNIQUE_CUSTOMERS'].sum():,}")

with col2:
    fig5 = px.area(filtered_data, x='ORDER_MONTH', y='TOTAL_REVENUE',
                   title=f'Revenue Trend ({selected_year})')
    st.plotly_chart(fig5, use_container_width=True)

st.success("✅ Dashboard loaded successfully from Snowflake TPC-H data!")
