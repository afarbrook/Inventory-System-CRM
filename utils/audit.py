import pandas as pd
from datetime import datetime
import streamlit as st
from utils.excel import get_supabase

def loadLog() -> pd.DataFrame:
    supabase = get_supabase()
    response = supabase.table("Audit_log").select("*").order("Timestamp", desc=True).execute()
    if not response.data:
        return pd.DataFrame(columns=["Timestamp", "User", "Action", "Row_ID", "Field", "Old_Value", "New_Value"])
    return pd.DataFrame(response.data)

def detectChanges(original, changed):
    changes = []

    deleted_ids = set(original.index) - set(changed.index)
    for row_id in deleted_ids:
        changes.append({
            "Timestamp": datetime.now().isoformat(),
            "User": st.session_state["username"],
            "Action": "deleted",
            "Row_ID": str(row_id),
            "Field": "-",
            "Old_Value": str(original.loc[row_id, "ItemID"]) if "ItemID" in original.columns else str(row_id),
            "New_Value": "-"
        })

    added_ids = set(changed.index) - set(original.index)
    for row_id in added_ids:
        changes.append({
            "Timestamp": datetime.now().isoformat(),
            "User": st.session_state["username"],
            "Action": "added",
            "Row_ID": str(row_id),
            "Field": "-",
            "Old_Value": "-",
            "New_Value": str(changed.loc[row_id, "ItemID"]) if "ItemID" in changed.columns else str(row_id),
        })

    for row in original.index:
        for col in original.columns:
            if row not in changed.index or col not in changed.columns:
                continue
            old = original.at[row, col]
            new = changed.at[row, col]
            if old != new:
                changes.append({
                    "Timestamp": datetime.now().isoformat(),
                    "User": st.session_state["username"],
                    "Action": "changed",
                    "Row_ID": str(row),
                    "Field": col,
                    "Old_Value": str(old.item()) if hasattr(old, 'item') else str(old),
                    "New_Value": str(new.item()) if hasattr(new, 'item') else str(new)
                })
    return changes

def log_action(action: str, detail: str):
    log({
        "Timestamp": datetime.now().isoformat(),
        "User": st.session_state["username"],
        "Action": action,
        "Row_ID": "-",
        "Field": "-",
        "Old_Value": "-",
        "New_Value": detail
    })

def log(change):
    supabase = get_supabase()
    supabase.table("Audit_log").insert(change).execute()