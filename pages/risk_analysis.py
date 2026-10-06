import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import (
    load_suppliers,
    load_products,
    load_orders,
    load_shipments,
    load_inventory
)

from utils.calculations import (
    calculate_order_value,
    calculate_supplier_performance,
    calculate_inventory_risk,
    calculate_shipment_metrics
)

from utils.risk_engine import calculate_supplier_risk


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SupplySense - Overall Risk",
    page_icon="⚠️",
    layout="wide"
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("⚠️ Supply Chain Risk Analysis")

st.write(
    "Overall view of supplier, inventory, and shipment "
    "risk across the supply chain."
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
# SUPPLIER RISK
# ---------------------------------------------------------

orders = calculate_order_value(orders)

supplier_performance = calculate_supplier_performance(
    suppliers,
    orders,
    shipments
)

supplier_risk = calculate_supplier_risk(
    supplier_performance
)


# ---------------------------------------------------------
# INVENTORY RISK
# ---------------------------------------------------------

inventory_risk = calculate_inventory_risk(
    inventory
)


# ---------------------------------------------------------
# SHIPMENT RISK
# ---------------------------------------------------------

shipment_metrics = calculate_shipment_metrics(
    shipments
)


# ---------------------------------------------------------
# SUPPLIER RISK METRICS
# ---------------------------------------------------------

total_suppliers = len(supplier_risk)

high_risk_suppliers = (
    supplier_risk["risk_category"] == "High Risk"
).sum()

medium_risk_suppliers = (
    supplier_risk["risk_category"] == "Medium Risk"
).sum()

low_risk_suppliers = (
    supplier_risk["risk_category"] == "Low Risk"
).sum()


# ---------------------------------------------------------
# INVENTORY RISK METRICS
# ---------------------------------------------------------

low_stock_products = (
    inventory_risk["stock_status"] == "Low Stock"
).sum()

overstock_products = (
    inventory_risk["stock_status"] == "Overstock"
).sum()

stockout_risk_products = (
    inventory_risk["stockout_risk"]
).sum()

overstock_risk_products = (
    inventory_risk["overstock_risk"]
).sum()


# ---------------------------------------------------------
# SHIPMENT RISK METRICS
# ---------------------------------------------------------

total_shipments = shipment_metrics["total_shipments"]

delayed_shipments = shipment_metrics["delayed_shipments"]

on_time_rate = shipment_metrics["on_time_rate"]

average_delay = shipment_metrics["average_delay_days"]


# ---------------------------------------------------------
# OVERALL RISK SCORE
# ---------------------------------------------------------

supplier_risk_percentage = (
    high_risk_suppliers / total_suppliers
) * 100

inventory_risk_percentage = (
    stockout_risk_products / len(inventory_risk)
) * 100

shipment_risk_percentage = 100 - on_time_rate

overall_risk_score = (
    supplier_risk_percentage * 0.40
    + inventory_risk_percentage * 0.30
    + shipment_risk_percentage * 0.30
)

overall_risk_score = round(
    overall_risk_score,
    2
)


# ---------------------------------------------------------
# OVERALL RISK CATEGORY
# ---------------------------------------------------------

if overall_risk_score < 30:
    overall_risk_category = "Low Risk"
elif overall_risk_score < 60:
    overall_risk_category = "Medium Risk"
else:
    overall_risk_category = "High Risk"


# ---------------------------------------------------------
# OVERALL RISK SUMMARY
# ---------------------------------------------------------

st.subheader("Overall Supply Chain Risk")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Overall Risk Score",
        f"{overall_risk_score:.2f}"
    )

with col2:
    st.metric(
        "Overall Risk Level",
        overall_risk_category
    )

with col3:
    st.metric(
        "High-Risk Suppliers",
        f"{high_risk_suppliers:,}"
    )

with col4:
    st.metric(
        "Stockout Risk Products",
        f"{stockout_risk_products:,}"
    )


st.divider()


# ---------------------------------------------------------
# RISK COMPONENTS
# ---------------------------------------------------------

st.subheader("Risk Components")

risk_components = pd.DataFrame(
    {
        "Risk Area": [
            "Supplier Risk",
            "Inventory Risk",
            "Shipment Risk"
        ],
        "Risk Percentage": [
            supplier_risk_percentage,
            inventory_risk_percentage,
            shipment_risk_percentage
        ]
    }
)

risk_components["Risk Percentage"] = (
    risk_components["Risk Percentage"].round(2)
)

risk_component_chart = px.bar(
    risk_components,
    x="Risk Area",
    y="Risk Percentage",
    title="Risk by Supply Chain Area",
    text="Risk Percentage"
)

risk_component_chart.update_layout(
    xaxis_title="Risk Area",
    yaxis_title="Risk Percentage (%)"
)

st.plotly_chart(
    risk_component_chart,
    width="stretch"
)


# ---------------------------------------------------------
# SUPPLIER RISK DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Supplier Risk Distribution")

supplier_risk_counts = (
    supplier_risk["risk_category"]
    .value_counts()
    .reset_index()
)

supplier_risk_counts.columns = [
    "Risk Category",
    "Supplier Count"
]

supplier_risk_chart = px.pie(
    supplier_risk_counts,
    names="Risk Category",
    values="Supplier Count",
    title="Supplier Risk Categories",
    hole=0.4
)

st.plotly_chart(
    supplier_risk_chart,
    width="stretch"
)


# ---------------------------------------------------------
# INVENTORY RISK SUMMARY
# ---------------------------------------------------------

st.subheader("Inventory Risk Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Low Stock Products",
        f"{low_stock_products:,}"
    )

with col2:
    st.metric(
        "Stockout Risk Products",
        f"{stockout_risk_products:,}"
    )

with col3:
    st.metric(
        "Overstock Risk Products",
        f"{overstock_risk_products:,}"
    )


# ---------------------------------------------------------
# SHIPMENT RISK SUMMARY
# ---------------------------------------------------------

st.subheader("Shipment Risk Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Shipments",
        f"{total_shipments:,}"
    )

with col2:
    st.metric(
        "Delayed Shipments",
        f"{delayed_shipments:,}"
    )

with col3:
    st.metric(
        "Average Delay",
        f"{average_delay:.2f} days"
    )


st.metric(
    "On-Time Delivery Rate",
    f"{on_time_rate:.2f}%"
)


# ---------------------------------------------------------
# TOP RISK SUPPLIERS
# ---------------------------------------------------------

st.divider()

st.subheader("Top Risk Suppliers")

top_risk_suppliers = (
    supplier_risk
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(10)
)

top_risk_display = top_risk_suppliers[
    [
        "supplier_name",
        "risk_score",
        "risk_category",
        "on_time_rate",
        "average_delay_days",
        "defect_rate"
    ]
].copy()

st.dataframe(
    top_risk_display,
    width="stretch",
    hide_index=True
)


# ---------------------------------------------------------
# RISK ALERTS
# ---------------------------------------------------------

st.divider()

st.subheader("⚠️ Risk Alerts")

if high_risk_suppliers > 0:
    st.warning(
        f"{high_risk_suppliers} supplier(s) are classified "
        "as high risk and require attention."
    )
else:
    st.success(
        "No suppliers are currently classified as high risk."
    )


if stockout_risk_products > 0:
    st.warning(
        f"{stockout_risk_products} product(s) have potential "
        "stockout risk."
    )
else:
    st.success(
        "No products currently show stockout risk."
    )


if delayed_shipments > 0:
    st.warning(
        f"{delayed_shipments} shipment(s) have been delayed."
    )
else:
    st.success(
        "No shipment delays have been detected."
    )


# ---------------------------------------------------------
# RISK METHODOLOGY
# ---------------------------------------------------------

st.divider()

st.subheader("Overall Risk Methodology")

st.write(
    "The overall supply chain risk score combines three "
    "risk areas: supplier risk, inventory risk, and shipment risk."
)

st.write(
    "**Supplier Risk Weight: 40%**"
)

st.write(
    "**Inventory Risk Weight: 30%**"
)

st.write(
    "**Shipment Risk Weight: 30%**"
)

st.write(
    "Overall Risk Score below 30 is classified as Low Risk, "
    "30 to below 60 as Medium Risk, and 60 or above as High Risk."
)