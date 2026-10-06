import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_suppliers,
    load_orders,
    load_shipments
)

from utils.calculations import (
    calculate_order_value,
    calculate_supplier_performance
)

from utils.risk_engine import calculate_supplier_risk


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SupplySense - Supplier Risk",
    page_icon="🏭",
    layout="wide"
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("🏭 Supplier Risk Analysis")

st.write(
    "Analyze supplier performance, delivery reliability, "
    "defect rates, and overall supplier risk."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

suppliers = load_suppliers()
orders = load_orders()
shipments = load_shipments()


# ---------------------------------------------------------
# CALCULATE SUPPLIER PERFORMANCE
# ---------------------------------------------------------

orders = calculate_order_value(orders)

supplier_performance = calculate_supplier_performance(
    suppliers,
    orders,
    shipments
)


# ---------------------------------------------------------
# CALCULATE SUPPLIER RISK
# ---------------------------------------------------------

supplier_risk = calculate_supplier_risk(
    supplier_performance
)


# ---------------------------------------------------------
# RISK SUMMARY
# ---------------------------------------------------------

st.subheader("Supplier Risk Summary")

high_risk = (
    supplier_risk["risk_category"] == "High Risk"
).sum()

medium_risk = (
    supplier_risk["risk_category"] == "Medium Risk"
).sum()

low_risk = (
    supplier_risk["risk_category"] == "Low Risk"
).sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Suppliers",
        f"{len(supplier_risk):,}"
    )

with col2:
    st.metric(
        "High Risk",
        f"{high_risk:,}"
    )

with col3:
    st.metric(
        "Medium Risk",
        f"{medium_risk:,}"
    )

with col4:
    st.metric(
        "Low Risk",
        f"{low_risk:,}"
    )


st.divider()


# ---------------------------------------------------------
# RISK DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Risk Distribution")

risk_counts = (
    supplier_risk["risk_category"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk Category",
    "Supplier Count"
]

risk_chart = px.pie(
    risk_counts,
    names="Risk Category",
    values="Supplier Count",
    title="Supplier Risk Distribution",
    hole=0.4
)

st.plotly_chart(
    risk_chart,
    width="stretch"
)


# ---------------------------------------------------------
# RISK FILTER
# ---------------------------------------------------------

st.subheader("Supplier Risk Details")

risk_filter = st.selectbox(
    "Filter by Risk Category",
    [
        "All",
        "High Risk",
        "Medium Risk",
        "Low Risk"
    ]
)


filtered_data = supplier_risk.copy()

if risk_filter != "All":
    filtered_data = filtered_data[
        filtered_data["risk_category"] == risk_filter
    ]


# ---------------------------------------------------------
# SUPPLIER PERFORMANCE TABLE
# ---------------------------------------------------------

display_columns = [
    "supplier_id",
    "supplier_name",
    "location",
    "supplier_category",
    "total_orders",
    "total_shipments",
    "on_time_rate",
    "average_delay_days",
    "defect_rate",
    "risk_score",
    "risk_category"
]

display_data = filtered_data[display_columns].copy()

display_data["on_time_rate"] = (
    display_data["on_time_rate"].round(2)
)

display_data["average_delay_days"] = (
    display_data["average_delay_days"].round(2)
)

display_data["defect_rate"] = (
    display_data["defect_rate"].round(2)
)

display_data["risk_score"] = (
    display_data["risk_score"].round(2)
)

st.dataframe(
    display_data,
    width="stretch",
    hide_index=True
)


# ---------------------------------------------------------
# HIGH-RISK SUPPLIERS
# ---------------------------------------------------------

st.divider()

st.subheader("Highest-Risk Suppliers")

high_risk_suppliers = (
    supplier_risk
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(10)
)

high_risk_display = high_risk_suppliers[
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
    high_risk_display,
    width="stretch",
    hide_index=True
)


# ---------------------------------------------------------
# RISK SCORE CHART
# ---------------------------------------------------------

st.subheader("Supplier Risk Scores")

risk_score_chart = px.bar(
    high_risk_suppliers.sort_values(
        "risk_score",
        ascending=True
    ),
    x="risk_score",
    y="supplier_name",
    orientation="h",
    title="Top 10 Highest-Risk Suppliers",
    text="risk_score"
)

risk_score_chart.update_layout(
    xaxis_title="Risk Score",
    yaxis_title="Supplier"
)

st.plotly_chart(
    risk_score_chart,
    width="stretch"
)


# ---------------------------------------------------------
# RISK INTERPRETATION
# ---------------------------------------------------------

st.divider()

st.subheader("Risk Interpretation")

st.write(
    "**Risk Score:** A combined score based on delivery performance, "
    "average delay, defect rate, and supplier reliability."
)

st.write(
    "**Low Risk:** Risk score from 0 to 39."
)

st.write(
    "**Medium Risk:** Risk score from 40 to 69."
)

st.write(
    "**High Risk:** Risk score from 70 to 100."
)