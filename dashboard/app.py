import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Samsung Sales Dashboard", layout="wide")

st.title("📊 Samsung Global Sales Analytics Dashboard")

# Load dataset
df = pd.read_csv("../data/samsung_global_sales_dataset.csv")

# ---- SIDEBAR FILTERS ----

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

channel = st.sidebar.multiselect(
    "Sales Channel",
    options=df["sales_channel"].unique(),
    default=df["sales_channel"].unique()
)

category = st.sidebar.multiselect(
    "Product Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

# Apply filters
filtered_df = df[
    (df["region"].isin(region)) &
    (df["sales_channel"].isin(channel)) &
    (df["category"].isin(category))
]

# ---- KPI SECTION ----

total_revenue = filtered_df["revenue_usd"].sum()
total_units = filtered_df["units_sold"].sum()
avg_rating = filtered_df["customer_rating"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Units Sold", f"{total_units:,}")
col3.metric("Average Rating", f"{avg_rating:.2f}")

st.divider()

# ---- REVENUE BY REGION ----

region_sales = filtered_df.groupby("region")["revenue_usd"].sum().reset_index()

fig1 = px.bar(
    region_sales,
    x="region",
    y="revenue_usd",
    title="Revenue by Region",
    color="region"
)

st.plotly_chart(fig1, use_container_width=True)

# ---- MONTHLY SALES TREND ----

sales_trend = filtered_df.groupby("month")["revenue_usd"].sum().reset_index()

fig2 = px.line(
    sales_trend,
    x="month",
    y="revenue_usd",
    title="Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# ---- TOP PRODUCTS ----

top_products = (
    filtered_df.groupby("product_name")["units_sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="product_name",
    y="units_sold",
    title="Top 10 Products",
    color="units_sold"
)

st.plotly_chart(fig3, use_container_width=True)

# ---- SALES CHANNEL DISTRIBUTION ----

channel_sales = filtered_df.groupby("sales_channel")["revenue_usd"].sum().reset_index()

fig4 = px.pie(
    channel_sales,
    values="revenue_usd",
    names="sales_channel",
    title="Sales Channel Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.header("Key Business Insights")

# Top region
top_region = (
    filtered_df.groupby("region")["revenue_usd"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

# Top product
top_product = (
    filtered_df.groupby("product_name")["units_sold"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

# Best sales channel
top_channel = (
    filtered_df.groupby("sales_channel")["revenue_usd"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

# Average discount
avg_discount = filtered_df["discount_pct"].mean()

st.markdown(f"""
###  Insights from the Data

• **Top Revenue Region:** {top_region}

• **Best Selling Product:** {top_product}

• **Most Effective Sales Channel:** {top_channel}

• **Average Discount Offered:** {avg_discount:.2f}%

These insights help businesses understand **where sales are strongest and which products drive the most revenue.**
""")

st.divider()
st.header("Global Sales Map")

country_sales = (
    filtered_df.groupby("country", as_index=False)["revenue_usd"].sum()
)

fig_map = px.choropleth(
    country_sales,
    locations="country",
    locationmode="country names",
    color="revenue_usd",
    hover_name="country",
    color_continuous_scale="Blues",
    title="Global Revenue Distribution"
)

fig_map.update_layout(
    geo=dict(showframe=False, showcoastlines=True)
)

st.plotly_chart(fig_map, use_container_width=True)