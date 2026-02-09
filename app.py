import streamlit as st
from utils.excel import load_inventory
from utils.metrics import compute_metrics

st.set_page_config(
    page_title="Inventory Dashboard",
    layout="wide"
)

st.title("📦 Inventory Dashboard")

df = load_inventory()

if df.empty:
    st.warning("No inventory data found.")
    st.stop()

metrics = compute_metrics(df)

c1, c2, c3 = st.columns(3)
c1.metric("Total Items", metrics["total_items"])
c2.metric("Total Quantity", metrics["total_quantity"])
c3.metric("Low Stock Items", metrics["low_stock"])

st.subheader("Inventory by Category")
st.bar_chart(metrics["by_category"])

st.subheader("Recently Added Items")
st.dataframe(metrics["recent_items"], use_container_width=True)
