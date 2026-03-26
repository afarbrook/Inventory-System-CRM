import streamlit as st
from utils.audit import loadLog

st.header("Audit Log")

df = loadLog()
st.dataframe(df)