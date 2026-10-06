import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_suppliers,
    load_products,
    load_orders,
    load_shipments,
    load_inventory
)

from utils.calculations import (
    calculate_order_value,
    calculate_shipment_metrics,
    calculate_supplier_performance,
    calculate_inventory_status
)

from utils.risk_engine import calculate_supplier_risk


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SupplySense - Dashboard",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("📊 Executive Dashboard")

st.write(
    "Overview of suppliers, products, orders, inventory, "
    "shipments, and supply chain risk."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

suppliers = load_suppliers()
products = load_products()
orders = load_orders()
shipments = load_shipments()
inventory = load_inventory()


# ---------------------------------------------------------
# CALCULATE BUSINESS METRICS
# ---------------------------------------------------------

orders = calculate_order_value(orders)

shipment_metrics = calculate_shipment_metrics(shipments)

supplier_performance = calculate_supplier_performance(
    suppliers,
    orders,
    shipments
)

supplier_risk = calculate_supplier_risk(
    supplier_performance
)

inventory_status = calculate_inventory_status(
    inventory
)


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

total_suppliers = len(suppliers)

total_products = len(products)

total_orders = len(orders)

total_shipments = len(shipments)

total_order_value = orders["order_value"].sum()

on_time_rate = shipment_metrics["on_time_rate"]


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Suppliers",
        f"{total_suppliers:,}"
    )

with col2:
    st.metric(
        "Total Products",
        f"{total_products:,}"
    )

with col3:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col4:
    st.metric(
        "Total Shipments",
        f"{total_shipments:,}"
    )


col5, col6 = st.columns(2)

with col5:
    st.metric(
        "Total Order Value",
        f"₹{total_order_value:,.0f}"
    )

with col6:
    st.metric(
        "On-Time Delivery Rate",
        f"{on_time_rate:.2f}%"
    )


st.divider()


# ---------------------------------------------------------
# SUPPLIER RISK OVERVIEW
# ---------------------------------------------------------

st.subheader("Supplier Risk Overview")

risk_counts = (
    supplier_risk["risk_category"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = ["Risk Category", "Supplier Count"]

risk_chart = px.bar(
    risk_counts,
    x="Risk Category",
    y="Supplier Count",
    title="Suppliers by Risk Category",
    text="Supplier Count"
)

risk_chart.update_layout(
    xaxis_title="Risk Category",
    yaxis_title="Number of Suppliers"
)

st.plotly_chart(
    risk_chart,
    width="stretch"
)


# ---------------------------------------------------------
# INVENTORY OVERVIEW
# ---------------------------------------------------------

st.subheader("Inventory Overview")

inventory_counts = (
    inventory_status["stock_status"]
    .value_counts()
    .reset_index()
)

inventory_counts.columns = ["Stock Status", "Product Count"]

inventory_chart = px.pie(
    inventory_counts,
    names="Stock Status",
    values="Product Count",
    title="Inventory Status Distribution",
    hole=0.4
)

st.plotly_chart(
    inventory_chart,
    width="stretch"
)


# ---------------------------------------------------------
# SHIPMENT PERFORMANCE
# ---------------------------------------------------------

st.subheader("Shipment Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "On-Time Shipments",
        f"{shipment_metrics['on_time_shipments']:,}"
    )

with col2:
    st.metric(
        "Delayed Shipments",
        f"{shipment_metrics['delayed_shipments']:,}"
    )

with col3:
    st.metric(
        "Average Delay",
        f"{shipment_metrics['average_delay_days']:.2f} days"
    )


# ---------------------------------------------------------
# TOP SUPPLIERS
# ---------------------------------------------------------

st.subheader("Top Suppliers by Order Value")

supplier_order_value = (
    orders.groupby("supplier_id")
    .agg(
        total_order_value=("order_value", "sum"),
        total_orders=("order_id", "count")
    )
    .reset_index()
)

top_suppliers = supplier_order_value.merge(
    suppliers[
        ["supplier_id", "supplier_name"]
    ],
    on="supplier_id",
    how="left"
)

top_suppliers = top_suppliers.sort_values(
    "total_order_value",
    ascending=False
).head(10)

top_supplier_chart = px.bar(
    top_suppliers,
    x="total_order_value",
    y="supplier_name",
    orientation="h",
    title="Top 10 Suppliers by Order Value",
    text="total_order_value"
)

top_supplier_chart.update_layout(
    xaxis_title="Order Value (₹)",
    yaxis_title="Supplier"
)

st.plotly_chart(
    top_supplier_chart,
    width="stretch"
)


# ---------------------------------------------------------
# DASHBOARD SUMMARY
# ---------------------------------------------------------

st.divider()

st.subheader("Supply Chain Summary")

high_risk_count = (
    supplier_risk["risk_category"] == "High Risk"
).sum()

low_stock_count = (
    inventory_status["stock_status"] == "Low Stock"
).sum()

overstock_count = (
    inventory_status["stock_status"] == "Overstock"
).sum()

st.write(
    f"**{high_risk_count} suppliers** are currently classified "
    f"as high risk based on delivery, delay, defect, and reliability metrics."
)

st.write(
    f"**{low_stock_count} products** are below their reorder level "
    f"and may require inventory attention."
)

st.write(
    f"**{overstock_count} products** are classified as overstocked "
    f"based on the current inventory rules."
)