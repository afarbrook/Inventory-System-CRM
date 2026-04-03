import pandas as pd
from pathlib import Path
from datetime import datetime
import streamlit as st

AUDIT_PATH = Path("data/AuditLog.xlsx")
"""
loadLog() -- loads the audit log from the Excel file
@return -- a DataFrame containing the audit log, or None if the file doesn't exist
"""
def loadLog() -> pd.DataFrame:
    if(AUDIT_PATH.exists()):
        df = pd.read_excel(
            AUDIT_PATH,
            engine="openpyxl"
        )
        return df
        
    return None

"""
detectChanges(original, changed) -- detects changes between two DataFrames
@param -- original is the original DataFrame, changed is the modified DataFrame
"""
def detectChanges(original, changed):
    changes = []
    for row in original.index:
        for col in original.columns:
            if row not in changed.index or col not in changed.columns:
                continue
            old = original.at[row, col]
            new = changed.at[row,col]
            if old!=new:
               changes.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "User": st.session_state["username"],
                    "Action": "changed",
                    "Row_ID": row,
                    "Field": col,
                    "Old_Value": old.item() if hasattr(old, 'item') else old,  # convert np types to python native
                    "New_Value": new.item() if hasattr(new, 'item') else new
                })
    return changes 
"""
log(change) -- logs a change to the audit log
@param -- change is a dictionary containing the change details
"""
def log(change):
    df = loadLog()
    if df is None:
        AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(columns=["Timestamp", "User", "Action", "Row_ID", "Field", "Old_Value", "New_Value"])
        
    newRow = pd.DataFrame([change])
    df = pd.concat([df, newRow], ignore_index=True)
    df.to_excel(AUDIT_PATH, index=False, engine="openpyxl")

