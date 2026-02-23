import streamlit as st
import pandas as pd
from utils.excel import load_inventory
df = load_inventory()
st.header("🔍 Inventory Search")

search_query = st.text_input(
    "Search (Item name, ID, location, category)",
    placeholder="e.g. laptop, IT-203, warehouse A"
)

col1, col2, col3 = st.columns(3)

with col1:
    category = st.selectbox(
        "Category",
        ["All"] + sorted(df["Category"].dropna().unique().tolist())
    )

with col2:
    min_qty = st.number_input("Min Quantity", min_value=0, value=0)

with col3:
    max_qty = st.number_input(
        "Max Quantity",
        min_value=0,
        value=int(df["Quantity"].max())
    )

filtered_df = df.copy()

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: q in " ".join(
                str(row[col]).lower()
                for col in ["ItemID", "ItemName", "Location", "Category"]
                if col in row
            ),
            axis=1
        )
    ]

if category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category]

filtered_df = filtered_df[
    (filtered_df["Quantity"] >= min_qty) &
    (filtered_df["Quantity"] <= max_qty)
]

st.subheader(f"Results ({len(filtered_df)} items)")
st.dataframe(
    filtered_df,
    use_container_width=True
)