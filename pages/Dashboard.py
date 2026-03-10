import streamlit as st
from utils.excel import load_inventory
from utils.metrics import compute_metrics
from utils.alerts import get_expiring_warranties

def reset_app():
    st.session_state["logged in"] = False
    del st.session_state["username"]

st.button("Log Out", on_click=reset_app)

st.title("📦 Inventory Dashboard")

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()


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

#alert system in app
expiring_df = get_expiring_warranties(df, days=30)

if not expiring_df.empty:
    st.warning(
        f"⚠️ {len(expiring_df)} warranties expiring in next 30 days!"
    )
    st.dataframe(expiring_df)
st.set_page_config(
    page_title="Inventory Dashboard",
    layout="wide"
)