import streamlit as st
import pandas as pd
from utils.audit import loadLog

st.header("Audit Log")

df = loadLog()
st.dataframe(df)