import pandas as pd
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

@st.cache_data(ttl=60)
def load_inventory() -> pd.DataFrame:
    supabase = get_supabase()
    all_rows = []
    page_size = 1000
    offset = 0
    while True:
        response = supabase.table("Inventory").select("*").order("ItemID").range(offset, offset + page_size - 1).execute()
        if not response.data:
            break
        all_rows.extend(response.data)
        if len(response.data) < page_size:
            break
        offset += page_size

    if not all_rows:
        return pd.DataFrame(columns=[
            "ItemID", "ItemName", "Category", "Quantity", "Location", "AssignedTo",
            "DateAdded", "LastUpdated", "Brand", "ModelNumber",
            "SerialNumber", "Cost", "Status",
            "WarrantyExpiration", "WarrantyProvider", "Notes"
        ])
    df = pd.DataFrame(all_rows)
    df["DateAdded"] = pd.to_datetime(df["DateAdded"], errors="coerce")
    df["LastUpdated"] = pd.to_datetime(df["LastUpdated"], errors="coerce")
    df["WarrantyExpiration"] = pd.to_datetime(df["WarrantyExpiration"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    df["AssignedTo"] = df["AssignedTo"].fillna("").astype(str)
    return df

def save_inventory(df: pd.DataFrame):
    supabase = get_supabase()
    df = df.copy()
    df["LastUpdated"] = pd.Timestamp.now().isoformat()

    for col in ["DateAdded", "WarrantyExpiration"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].where(df[col].notna(), other=None)
            df[col] = df[col].apply(lambda x: x.isoformat() if pd.notna(x) else None)

    records = df.where(df.notna(), other=None).to_dict(orient="records")
    supabase.table("Inventory").upsert(records, on_conflict="ItemID").execute()
    st.cache_data.clear()

def append_inventory(existing: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat([existing, new], ignore_index=True)
    combined = combined.drop_duplicates(subset="ItemID", keep="last")
    return combined