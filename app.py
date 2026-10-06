import streamlit as st


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="SupplySense",
    page_icon="📦",
    layout="wide"
)


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

st.sidebar.title("📦 SupplySense")

st.sidebar.write(
    "Supply Chain Risk Platform"
)

st.sidebar.divider()

st.sidebar.info(
    "Use the pages in the sidebar "
    "to explore supply chain data."
)


# -----------------------------------------
# MAIN PAGE
# -----------------------------------------

st.title("📦 SupplySense")

st.subheader(
    "Supply Chain Risk Platform"
)

st.write(
    "Monitor suppliers, inventory, shipments, "
    "and overall supply chain risks."
)

st.success(
    "SupplySense application is running successfully!"
)


# -----------------------------------------
# PROJECT STATUS
# -----------------------------------------

st.divider()

st.subheader("Application Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Supplier Analysis",
        "Ready"
    )

with col2:
    st.metric(
        "Inventory Analysis",
        "Ready"
    )

with col3:
    st.metric(
        "Shipment Analysis",
        "Ready"
    )

st.write("")

st.info(
    "Detailed dashboards and risk analysis "
    "will be added in the upcoming phases."
)