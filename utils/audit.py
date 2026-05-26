import pandas as pd
from pathlib import Path
from datetime import datetime
import streamlit as st

AUDIT_PATH = Path("data/AuditLog.xlsx")

def loadLog() -> pd.DataFrame:
    if AUDIT_PATH.exists():
        return pd.read_excel(AUDIT_PATH, engine="openpyxl")
    return None

def detectChanges(original, changed):
    changes = []

    # detect deleted rows
    deleted_ids = set(original.index) - set(changed.index)
    for row_id in deleted_ids:
        changes.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "User": st.session_state["username"],
            "Action": "deleted",
            "Row_ID": row_id,
            "Field": "-",
            "Old_Value": str(original.loc[row_id, "ItemID"]) if "ItemID" in original.columns else str(row_id),
            "New_Value": "-"
        })

    # detect added rows
    added_ids = set(changed.index) - set(original.index)
    for row_id in added_ids:
        changes.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "User": st.session_state["username"],
            "Action": "added",
            "Row_ID": row_id,
            "Field": "-",
            "Old_Value": "-",
            "New_Value": str(changed.loc[row_id, "ItemID"]) if "ItemID" in changed.columns else str(row_id),
        })

    # detect changed cells
    for row in original.index:
        for col in original.columns:
            if row not in changed.index or col not in changed.columns:
                continue
            old = original.at[row, col]
            new = changed.at[row, col]
            if old != new:
                changes.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "User": st.session_state["username"],
                    "Action": "changed",
                    "Row_ID": row,
                    "Field": col,
                    "Old_Value": str(old.item()) if hasattr(old, 'item') else old,
                    "New_Value": str(new.item()) if hasattr(new, 'item') else new
                })
    return changes

def log_action(action: str, detail: str):
    """For discrete events like account creation/deletion."""
    log({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": st.session_state["username"],
        "Action": action,
        "Row_ID": "-",
        "Field": "-",
        "Old_Value": "-",
        "New_Value": detail
    })

def log(change):
    df = loadLog()
    if df is None:
        AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(columns=["Timestamp", "User", "Action", "Row_ID", "Field", "Old_Value", "New_Value"])
    newRow = pd.DataFrame([change])
    df = pd.concat([df, newRow], ignore_index=True)
    df.to_excel(AUDIT_PATH, index=False, engine="openpyxl")