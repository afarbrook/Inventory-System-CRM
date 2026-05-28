import pandas as pd
from datetime import datetime
from utils.excel import get_supabase
import streamlit as st

REQUIRED_COLUMNS = {
    "ItemID",
    "ItemName",
    "Category",
    "Quantity"
}

EXPECTED_TYPES = {
    "Quantity": "numeric",
    "Cost":     "numeric",
    "DateAdded": "date",
    "WarrantyExpiration": "date",
}

COLUMN_RENAMES = {
    "Warranty Expiration Date": "WarrantyExpiration",
    "Service Tag":              "SerialNumber",
    "Purchase Date":            "DateAdded",
    "Manufacturer":             "Brand",
}

def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    if uploaded_file.name.endswith(".csv"):
        try:
            return pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding="latin-1")
    elif uploaded_file.name.endswith(".xlsx"):
        xl = pd.ExcelFile(uploaded_file)
        sheet = xl.sheet_names[0]
        df = xl.parse(sheet)
        return df.rename(columns=COLUMN_RENAMES)
    else:
        raise ValueError("Unsupported file type. Please upload a .csv or .xlsx file.")

def validate_import_df(df: pd.DataFrame) -> list[str]:
    errors = []

    missing = REQUIRED_COLUMNS - set(df.columns)
    for col in missing:
        errors.append(f"Missing required column: **{col}**")

    if errors:
        return errors

    for col in REQUIRED_COLUMNS:
        if df[col].isnull().any():
            count = df[col].isnull().sum()
            errors.append(f"**{col}** has {count} empty row(s) — all required fields must be filled.")

    for col, kind in EXPECTED_TYPES.items():
        if col not in df.columns:
            continue
        if kind == "numeric":
            coerced = pd.to_numeric(df[col], errors="coerce")
            bad = coerced.isnull() & df[col].notnull()
            if bad.any():
                errors.append(f"**{col}** has {bad.sum()} non-numeric value(s).")
        elif kind == "date":
            coerced = pd.to_datetime(df[col], errors="coerce")
            bad = coerced.isnull() & df[col].notnull()
            if bad.any():
                errors.append(f"**{col}** has {bad.sum()} invalid date(s).")

    dupes = df["ItemID"].duplicated().sum()
    if dupes:
        errors.append(f"**ItemID** has {dupes} duplicate(s) — each item must have a unique ID.")

    return errors

def normalize_import_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "DateAdded" not in df.columns:
        df["DateAdded"] = datetime.today()
    df["DateAdded"] = pd.to_datetime(df["DateAdded"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    return df

def import_df_to_supabase(df: pd.DataFrame):
    supabase = get_supabase()

    for col in ["DateAdded", "WarrantyExpiration"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].apply(lambda x: x.isoformat() if pd.notna(x) else None)

    df["LastUpdated"] = datetime.now().isoformat()
    records = df.where(df.notna(), other=None).to_dict(orient="records")

    batch_size = 500
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        supabase.table("inventory").upsert(batch, on_conflict="ItemID").execute()

    st.cache_data.clear()