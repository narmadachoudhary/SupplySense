import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_shipments


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SupplySense - Shipment Analysis",
    page_icon="🚚",
    layout="wide"
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("🚚 Shipment Analysis")

st.write(
    "Analyze shipment performance, delivery delays, "
    "on-time delivery, and shipment destinations."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

shipments = load_shipments()


# ---------------------------------------------------------
# PREPARE DATE COLUMNS
# ---------------------------------------------------------

shipments["order_date"] = pd.to_datetime(
    shipments["order_date"]
)

shipments["expected_delivery_date"] = pd.to_datetime(
    shipments["expected_delivery_date"]
)

shipments["actual_delivery_date"] = pd.to_datetime(
    shipments["actual_delivery_date"]
)


# ---------------------------------------------------------
# SHIPMENT METRICS
# ---------------------------------------------------------

total_shipments = len(shipments)

on_time_shipments = (
    shipments["delivery_status"] == "On Time"
).sum()

delayed_shipments = (
    shipments["delivery_status"] == "Delayed"
).sum()

if total_shipments > 0:
    on_time_rate = (
        on_time_shipments / total_shipments
    ) * 100
else:
    on_time_rate = 0

average_delay = shipments["delay_days"].mean()


# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("Shipment Performance Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Shipments",
        f"{total_shipments:,}"
    )

with col2:
    st.metric(
        "On-Time Shipments",
        f"{on_time_shipments:,}"
    )

with col3:
    st.metric(
        "Delayed Shipments",
        f"{delayed_shipments:,}"
    )

with col4:
    st.metric(
        "On-Time Delivery Rate",
        f"{on_time_rate:.2f}%"
    )


col5 = st.columns(1)[0]

with col5:
    st.metric(
        "Average Delay",
        f"{average_delay:.2f} days"
    )


st.divider()


# ---------------------------------------------------------
# DELIVERY STATUS DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Delivery Status Distribution")

status_counts = (
    shipments["delivery_status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Delivery Status",
    "Shipment Count"
]

status_chart = px.pie(
    status_counts,
    names="Delivery Status",
    values="Shipment Count",
    title="On-Time vs Delayed Shipments",
    hole=0.4
)

st.plotly_chart(
    status_chart,
    width="stretch"
)


# ---------------------------------------------------------
# DELAY DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Shipment Delay Distribution")

delay_chart = px.histogram(
    shipments,
    x="delay_days",
    nbins=10,
    title="Distribution of Shipment Delays",
    labels={
        "delay_days": "Delay (Days)"
    }
)

delay_chart.update_layout(
    xaxis_title="Delay (Days)",
    yaxis_title="Number of Shipments"
)

st.plotly_chart(
    delay_chart,
    width="stretch"
)


# ---------------------------------------------------------
# DESTINATION ANALYSIS
# ---------------------------------------------------------

st.subheader("Shipments by Destination")

destination_counts = (
    shipments["destination"]
    .value_counts()
    .reset_index()
)

destination_counts.columns = [
    "Destination",
    "Shipment Count"
]

destination_chart = px.bar(
    destination_counts,
    x="Destination",
    y="Shipment Count",
    title="Shipment Volume by Destination",
    text="Shipment Count"
)

destination_chart.update_layout(
    xaxis_title="Destination",
    yaxis_title="Number of Shipments"
)

st.plotly_chart(
    destination_chart,
    width="stretch"
)


# ---------------------------------------------------------
# STATUS FILTER
# ---------------------------------------------------------

st.divider()

st.subheader("Shipment Details")

status_filter = st.selectbox(
    "Filter by Delivery Status",
    [
        "All",
        "On Time",
        "Delayed"
    ]
)


filtered_shipments = shipments.copy()

if status_filter != "All":
    filtered_shipments = filtered_shipments[
        filtered_shipments["delivery_status"] == status_filter
    ]


# ---------------------------------------------------------
# SHIPMENT TABLE
# ---------------------------------------------------------

display_columns = [
    "shipment_id",
    "order_id",
    "supplier_id",
    "product_id",
    "origin",
    "destination",
    "order_date",
    "expected_delivery_date",
    "actual_delivery_date",
    "delivery_status",
    "delay_days"
]

display_data = filtered_shipments[
    display_columns
].copy()

display_data["order_date"] = (
    display_data["order_date"]
    .dt.strftime("%Y-%m-%d")
)

display_data["expected_delivery_date"] = (
    display_data["expected_delivery_date"]
    .dt.strftime("%Y-%m-%d")
)

display_data["actual_delivery_date"] = (
    display_data["actual_delivery_date"]
    .dt.strftime("%Y-%m-%d")
)

st.dataframe(
    display_data,
    width="stretch",
    hide_index=True
)


# ---------------------------------------------------------
# HIGHEST DELAY SHIPMENTS
# ---------------------------------------------------------

st.divider()

st.subheader("Highest-Delay Shipments")

highest_delay = (
    shipments
    .sort_values(
        "delay_days",
        ascending=False
    )
    .head(10)
)

highest_delay_display = highest_delay[
    [
        "shipment_id",
        "supplier_id",
        "product_id",
        "origin",
        "destination",
        "delay_days",
        "delivery_status"
    ]
].copy()

st.dataframe(
    highest_delay_display,
    width="stretch",
    hide_index=True
)


# ---------------------------------------------------------
# SUPPLIER DELAY ANALYSIS
# ---------------------------------------------------------

st.subheader("Average Delay by Supplier")

supplier_delay = (
    shipments
    .groupby("supplier_id")
    .agg(
        average_delay_days=("delay_days", "mean"),
        total_shipments=("shipment_id", "count")
    )
    .reset_index()
    .sort_values(
        "average_delay_days",
        ascending=False
    )
    .head(10)
)

supplier_delay_chart = px.bar(
    supplier_delay,
    x="average_delay_days",
    y="supplier_id",
    orientation="h",
    title="Top 10 Suppliers by Average Shipment Delay",
    text="average_delay_days"
)

supplier_delay_chart.update_layout(
    xaxis_title="Average Delay (Days)",
    yaxis_title="Supplier"
)

st.plotly_chart(
    supplier_delay_chart,
    width="stretch"
)


# ---------------------------------------------------------
# INTERPRETATION
# ---------------------------------------------------------

st.divider()

st.subheader("Shipment Risk Interpretation")

st.write(
    "**On-Time Delivery Rate** measures the percentage "
    "of shipments delivered without delay."
)

st.write(
    "**Average Delay** represents the average number "
    "of days shipments were delayed."
)

st.write(
    "Suppliers with consistently higher shipment delays "
    "may require closer monitoring in the supplier risk analysis."
)