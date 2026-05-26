import streamlit as st
from utils.excel import load_inventory
from utils.metrics import compute_metrics
from utils.alerts import get_expiring_warranties

st.set_page_config(page_title="Inventory Dashboard", layout="wide")

def reset_app():
    st.session_state["logged in"] = False
    del st.session_state["username"]

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

st.button("Log Out", on_click=reset_app)
st.title("📦 Inventory Dashboard")

df = load_inventory()
if df.empty:
    st.warning("No inventory data found.")
    st.stop()

metrics = compute_metrics(df)

c1, c2, c3 = st.columns(3)
c1.metric("Total Items",    metrics["total_items"])
c2.metric("Total Quantity", metrics["total_quantity"])
c3.metric("Low Stock Items",metrics["low_stock"])

st.divider()

st.subheader("Inventory by Category")
st.bar_chart(metrics["by_category"])

st.subheader("Recently Added Items")
st.dataframe(metrics["recent_items"], use_container_width=True)

# warranty alerts — max 3 toasts
expiring = get_expiring_warranties(df, days=30)
if expiring.empty:
    st.toast("✅ No urgent warranties!")
else:
    for _, row in expiring.head(3).iterrows():
        st.toast(f"⚠️ {row['ItemName']} — warranty expires {row['WarrantyExpiration']}")
    if len(expiring) > 3:
        st.toast(f"...and {len(expiring) - 3} more expiring soon. Check Reports.")