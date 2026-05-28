import bcrypt
import pandas as pd
import streamlit as st
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
        "Role": "user"
    }).execute()

def hashPassword(password):
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode()

def checkAdmin():
    supabase = get_supabase()
    username = st.session_state["username"]
    response = supabase.table("Login_info").select("Role").eq("Username", username).execute()
    if not response.data:
        return False
    return response.data[0]["Role"] == "admin"

def load_users() -> pd.DataFrame:
    supabase = get_supabase()
    response = supabase.table("Login_info").select("Username, Role").execute()
    if not response.data:
        return pd.DataFrame(columns=["Username", "Role"])
    return pd.DataFrame(response.data)