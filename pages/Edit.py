import streamlit as st

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()

