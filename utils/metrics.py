import pandas as pd
import streamlit as st

@st.cache_data
def compute_metrics(df: pd.DataFrame):
    return {
        "total_items": len(df),
        "total_quantity": int(df["Quantity"].sum()),
        "low_stock": int((df["Quantity"] < 5).sum()),
        "recent_items": df.sort_values(
            "DateAdded",
            ascending=False
        ).head(5),
        "by_category": df.groupby("Category")["Quantity"].sum()
    }
