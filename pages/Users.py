import streamlit as st
import pandas as pd
from utils.accounts import load_users
from utils.accounts import checkAdmin

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

if(not checkAdmin()):
    st.error("Admin only!")
    st.stop()
st.set_page_config(page_title="User List", layout="wide")
st.title("User List")


df = load_users()
st.dataframe(df)



