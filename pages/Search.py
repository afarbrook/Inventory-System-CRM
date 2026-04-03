import streamlit as st
import pandas as pd
from utils.excel import load_inventory

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

df = load_inventory()

st.title("Inventory Search")
st.divider()

search_query = st.text_input("Search", placeholder="Item name, ID, location, category...")

col1, col2, col3 = st.columns(3)

with col1:
    category_filter = st.selectbox("Category", ["All"] + sorted(df["Category"].dropna().unique().tolist()))

with col2:
    min_qty = st.number_input("Min Quantity", min_value=0, value=0)

with col3:
    max_qty = st.number_input("Max Quantity", min_value=0, value=int(df["Quantity"].max()))

filtered_df = df.copy()

if search_query:
    query = search_query.lower()
    search_cols = ["ItemID", "ItemName", "Location", "Category"]
    filtered_df = filtered_df[
        filtered_df[search_cols].apply(
            lambda row: query in " ".join(row.astype(str).str.lower()), axis=1
        )
    ]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

filtered_df = filtered_df[
    (filtered_df["Quantity"] >= min_qty) &
    (filtered_df["Quantity"] <= max_qty)
]

st.subheader(f"Results — {len(filtered_df)} items found")
st.dataframe(filtered_df, use_container_width=True)