import bcrypt
import pandas as pd
import streamlit as st
from pathlib import Path
ACCOUNT_PATH = Path("data/LoginInfo.xlsx") #path for login info
SHEET_NAME = "Sheet1"

"""
login(username, password) -- checks if credentials are correct and return true if they are
@param -- username is the username, password is the password)
"""
def login(username, password) -> bool:
    if(ACCOUNT_PATH.exists()):
        df = pd.read_excel(
            ACCOUNT_PATH,
            engine="openpyxl"
        )
        accountRow = df[df["Username"] == username]
        if accountRow.empty:
            return False
        possiblePassword = accountRow.iloc[0]["Password"]
        return bcrypt.checkpw(password.encode(), possiblePassword.encode())
    return False

"""
createAccount(username, password) -- creates a new user account with the given username and password
@param -- username is the username, password is the password)
"""
def createAccount(username, password):
    if(ACCOUNT_PATH.exists()):
        df = pd.read_excel(
            ACCOUNT_PATH,
            engine="openpyxl"
        )
    else:
        df = pd.DataFrame(columns=["Username", "Password", "Role"])

    newRow = pd.DataFrame([{"Username":username, "Password":hashPassword(password.encode()), "Role":"user"}])
    df = pd.concat([df, newRow],ignore_index=True)
    df.to_excel(ACCOUNT_PATH, index=False, engine="openpyxl")

"""
hashPassword(password) -- hashes the given password
@param -- password is the password to hash)
"""
def hashPassword(password):
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode()
"""
checkAdmin(username, password) -- checks if the user is an admin
"""
def checkAdmin():
    df = pd.read_excel( #user account database
            ACCOUNT_PATH,
            engine="openpyxl"
        )
    username = st.session_state["username"] #username of current user
    accountRow = df[df["Username"] == username] #users row if exists
    role = accountRow.iloc[0]["Role"]
    return role == "admin"


@st.cache_data
def _load_users(path: Path, last_modified: float) -> pd.DataFrame:
    df = pd.read_excel(
        path,
        sheet_name=SHEET_NAME,
        engine="openpyxl",
        usecols=["Username", "Role"]
    )

    return df

def load_users() -> pd.DataFrame:
    if not ACCOUNT_PATH.exists():
        return pd.DataFrame(columns=[
            "Username", "Role"
        ])
    return _load_users(
        ACCOUNT_PATH,
        ACCOUNT_PATH.stat().st_mtime
    )