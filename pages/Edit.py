import streamlit as st
import pandas as pd
from utils.excel import load_inventory, save_inventory
from utils.audit import detectChanges, log
from utils.accounts import checkAdmin

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

if not checkAdmin():
    st.error("Admin only!")
    st.stop()

if st.session_state.get("just_saved"):
    st.session_state["just_saved"] = False

df = load_inventory()
st.set_page_config(page_title="Database Edit", layout="wide")
st.title("Database Edit")

newDF = st.data_editor(
    df,
    width="stretch",
    num_rows="dynamic",
    key="editor_key",
    column_config={
        "AssignedTo": st.column_config.TextColumn("Assigned To"),
        "DateAdded": st.column_config.DateColumn("Date Added"),
        "LastUpdated": st.column_config.DateColumn("Last Updated"),
        "WarrantyExpiration": st.column_config.DateColumn("Warranty Expiration"),
    }
)

if st.button("Save All Changes"):
    if not st.session_state.get("just_saved"):
        changes = detectChanges(df, newDF)
        for change in changes:
            log(change)
        save_inventory(newDF)
        st.session_state["just_saved"] = True
        st.success("Changes saved!")
        st.rerun()