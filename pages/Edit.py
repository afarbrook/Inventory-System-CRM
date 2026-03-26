import streamlit as st
import pandas as pd
from utils.excel import load_inventory, save_inventory
from utils.audit import detectChanges, log
from utils.accounts import checkAdmin
from pathlib import Path
from filelock import FileLock

"""
This page can edit the actual database, so it is admin only. User accounts are
'user' by default. For an admin account, please contact me
"""
SHEET_NAME = "LoginInfo"

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

if(not checkAdmin()):
    st.error("Admin only!")
    st.stop()

df = load_inventory() #full inventory

st.title("Database Edit")

newDF = st.data_editor(
    df, 
    width="stretch",
    num_rows="dynamic",
    key="editor_key"
    )

if st.button("Save All Changes"):
    changes = detectChanges(df, newDF)
    for change in changes:
        log(change)
    save_inventory(newDF)
    st.success("Changes saved!")
    st.cache_data.clear()