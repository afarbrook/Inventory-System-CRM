import bcrypt
import streamlit as st
import pandas as pd
from utils.excel import get_supabase

def login(username, password) -> bool:
    supabase = get_supabase()
    response = supabase.table("Login_info").select("Password").eq("Username", username).execute()
    if not response.data:
        return False
    stored_hash = response.data[0]["Password"]
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

def createAccount(username, password):
    supabase = get_supabase()
    supabase.table("Login_info").insert({
        "Username": username,
        "Password": hashPassword(password.encode()),
        "Admin": False
    }).execute()

def hashPassword(password):
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode()

def checkAdmin():
    supabase = get_supabase()
    username = st.session_state["username"]
    response = supabase.table("Login_info").select("Admin").eq("Username", username).execute()
    if not response.data:
        return False
    return response.data[0]["Admin"] == True

def load_users() -> pd.DataFrame:
    supabase = get_supabase()
    response = supabase.table("Login_info").select("Username", "Admin").execute()
    if not response.data:
        return pd.DataFrame(columns=["Username", "Admin"])
    return pd.DataFrame(response.data)