import streamlit as st
import pandas as pd
from utils.excel import load_inventory, save_inventory
from pathlib import Path
from filelock import FileLock

"""
This page can edit the actual database, so it is admin only. User accounts are
'user' by default. For an admin account, please contact me
"""
ACCOUNT_PATH = Path("data/LoginInfo.xlsx") #path for login info
SHEET_NAME = "LoginInfo"

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

if(not ACCOUNT_PATH.exists()): #checks if account file exists
    st.error("Account file missing")
    st.stop()

df = pd.read_excel(
    ACCOUNT_PATH,
    engine="openpyxl"
)

username = st.session_state["username"] #username of current user
accountRow = df[df["Username"] == username] #users row if exists
role = accountRow.iloc[0]["Role"] 
if role != "admin": #admin only page
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
    save_inventory(newDF)
    st.success("Changes saved!")
    st.cache_data.clear()