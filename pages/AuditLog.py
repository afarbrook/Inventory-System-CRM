import streamlit as st
from utils.audit import loadLog

st.set_page_config(page_title="Audit Log", layout="wide")

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

st.title("🗂️ Audit Log")

df = loadLog()

if df is None or df.empty:
    st.info("No audit activity recorded yet.")
    st.stop()

df = df.sort_values("Timestamp", ascending=False).reset_index(drop=True)

st.dataframe(
    df,
    use_container_width=True,
    height=600,
    column_config={
        "Timestamp":  st.column_config.TextColumn("Timestamp",  width="medium"),
        "User":       st.column_config.TextColumn("User",       width="small"),
        "Action":     st.column_config.TextColumn("Action",     width="small"),
        "Row_ID":     st.column_config.TextColumn("Row ID",     width="small"),
        "Field":      st.column_config.TextColumn("Field",      width="small"),
        "Old_Value":  st.column_config.TextColumn("Old Value",  width="medium"),
        "New_Value":  st.column_config.TextColumn("New Value",  width="medium"),
    }
)