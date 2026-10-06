import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_inventory,
    load_products
)

from utils.calculations import (
    calculate_inventory_risk
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SupplySense - Inventory Risk",
    page_icon="📦",
    layout="wide"
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("📦 Inventory Risk Analysis")

st.write(
    "Monitor inventory levels, stockout risk, overstock risk, "
    "and products requiring attention."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

inventory = load_inventory()
products = load_products()


# ---------------------------------------------------------
# CALCULATE INVENTORY RISK
# ---------------------------------------------------------

inventory_risk = calculate_inventory_risk(inventory)


# ---------------------------------------------------------
# ADD PRODUCT INFORMATION
# ---------------------------------------------------------

inventory_risk = inventory_risk.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "supplier_id"
        ]
    ],
    on="product_id",
    how="left"
)


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

total_products = len(inventory_risk)

low_stock = (
    inventory_risk["stock_status"] == "Low Stock"
).sum()

healthy_stock = (
    inventory_risk["stock_status"] == "Healthy"
).sum()

overstock = (
    inventory_risk["stock_status"] == "Overstock"
).sum()


# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("Inventory Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Products",
        f"{total_products:,}"
    )

with col2:
    st.metric(
        "Low Stock",
        f"{low_stock:,}"
    )

with col3:
    st.metric(
        "Healthy Stock",
        f"{healthy_stock:,}"
    )

with col4:
    st.metric(
        "Overstock",
        f"{overstock:,}"
    )


st.divider()


# ---------------------------------------------------------
# INVENTORY STATUS CHART
# ---------------------------------------------------------

st.subheader("Inventory Status Distribution")

status_counts = (
    inventory_risk["stock_status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Stock Status",
    "Product Count"
]

status_chart = px.pie(
    status_counts,
    names="Stock Status",
    values="Product Count",
    title="Products by Inventory Status",
    hole=0.4
)

st.plotly_chart(
    status_chart,
    width="stretch"
)


# ---------------------------------------------------------
# STOCKOUT AND OVERSTOCK RISK
# ---------------------------------------------------------

st.subheader("Inventory Risk Overview")

stockout_risk_count = (
    inventory_risk["stockout_risk"]
).sum()

overstock_risk_count = (
    inventory_risk["overstock_risk"]
).sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Stockout Risk Products",
        f"{stockout_risk_count:,}"
    )

with col2:
    st.metric(
        "Overstock Risk Products",
        f"{overstock_risk_count:,}"
    )


# ---------------------------------------------------------
# STOCK STATUS FILTER
# ---------------------------------------------------------

st.divider()

st.subheader("Inventory Details")

status_filter = st.selectbox(
    "Filter by Stock Status",
    [
        "All",
        "Low Stock",
        "Healthy",
        "Overstock"
    ]
)


filtered_inventory = inventory_risk.copy()

if status_filter != "All":
    filtered_inventory = filtered_inventory[
        filtered_inventory["stock_status"] == status_filter
    ]


# ---------------------------------------------------------
# INVENTORY TABLE
# ---------------------------------------------------------

display_columns = [
    "product_id",
    "product_name",
    "category",
    "supplier_id",
    "current_stock",
    "reorder_level",
    "average_daily_demand",
    "lead_time_days",
    "days_of_stock",
    "stock_status",
    "stockout_risk",
    "overstock_risk"
]

display_data = filtered_inventory[
    display_columns
].copy()

display_data["days_of_stock"] = (
    display_data["days_of_stock"].round(2)
)
st.dataframe(
    display_data,
    width="stretch",
    hide_index=True
)

# ---------------------------------------------------------
# PRODUCTS REQUIRING ATTENTION
# ---------------------------------------------------------

st.divider()

st.subheader("Products Requiring Attention")

attention_products = inventory_risk[
    (
        inventory_risk["stockout_risk"] == True
    )
    |
    (
        inventory_risk["overstock_risk"] == True
    )
].copy()

attention_products = attention_products.sort_values(
    "days_of_stock"
)

attention_display = attention_products[
    [
        "product_name",
        "category",
        "current_stock",
        "reorder_level",
        "average_daily_demand",
        "lead_time_days",
        "days_of_stock",
        "stock_status",
        "stockout_risk",
        "overstock_risk"
    ]
].copy()

attention_display["days_of_stock"] = (
    attention_display["days_of_stock"].round(2)
)

st.dataframe(
    attention_display,
    width="stretch",
    hide_index=True
)


# ---------------------------------------------------------
# DAYS OF STOCK CHART
# ---------------------------------------------------------

st.subheader("Days of Stock by Product")

top_inventory_risk = (
    inventory_risk
    .sort_values(
        "days_of_stock",
        ascending=True
    )
    .head(15)
)

days_stock_chart = px.bar(
    top_inventory_risk,
    x="days_of_stock",
    y="product_name",
    orientation="h",
    title="Products with Lowest Days of Stock",
    text="days_of_stock"
)

days_stock_chart.update_layout(
    xaxis_title="Days of Stock",
    yaxis_title="Product"
)

st.plotly_chart(
    days_stock_chart,
    width="stretch"
)


# ---------------------------------------------------------
# RISK INTERPRETATION
# ---------------------------------------------------------

st.divider()

st.subheader("Inventory Risk Interpretation")

st.write(
    "**Days of Stock** estimates how many days the current "
    "inventory can support based on average daily demand."
)

st.write(
    "**Stockout Risk** is identified when available stock "
    "is insufficient to cover the supplier lead time."
)

st.write(
    "**Overstock Risk** is identified when current stock "
    "is more than three times the reorder level."
)