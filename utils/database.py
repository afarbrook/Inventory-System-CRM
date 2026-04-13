"""
import psycopg2
import pandas as pd
import streamlit as st

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["SUPABASE_HOST"],
        database=st.secrets["SUPABASE_DB"],
        user=st.secrets["SUPABASE_USER"],
        password=st.secrets["SUPABASE_PASSWORD"],
        port=st.secrets["SUPABASE_PORT"]
    )

conn = get_connection()
"""