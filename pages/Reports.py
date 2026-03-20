import streamlit as st
import pandas as pd
from utils.reports import generate_report
from utils.excel import load_inventory

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

st.header("📄 Inventory Reports")
df = load_inventory()

categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())

col1, col2, col3 = st.columns(3)

with col1:
    selected_category = st.selectbox("Category", categories)

with col2:
    low_stock = st.checkbox("Low stock only (< 5)")

with col3:
    date_range = st.date_input(
        "Date range",
        value=(df["DateAdded"].min(), df["DateAdded"].max())
    )

start_date, end_date = date_range

report_df = generate_report(
    df,
    category=selected_category,
    low_stock_only=low_stock,
    start_date=start_date,
    end_date=end_date
)

st.subheader("Report Preview")
st.dataframe(report_df, use_container_width=True)