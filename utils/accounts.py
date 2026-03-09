import bcrypt
import pandas as pd
from pathlib import Path

ACCOUNT_PATH = Path("data/LoginInfo.xlsx") #path for login info
SHEET_NAME = "LoginInfo"


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


def createAccount(username, password):
    if(ACCOUNT_PATH.exists()):
        df = pd.read_excel(
            ACCOUNT_PATH,
            engine="openpyxl"
        )
    else:
        df = pd.DataFrame(columns=["Username", "Password"])

    newRow = pd.DataFrame([{"Username":username, "Password":hashPassword(password.encode())}])
    df = pd.concat([df, newRow],ignore_index=True)
    df.to_excel(ACCOUNT_PATH, index=False, engine="openpyxl")

   
def hashPassword(password):
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode()