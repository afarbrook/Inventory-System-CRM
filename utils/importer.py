import pandas as pd
from datetime import datetime

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

def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file, engine="openpyxl")
    else:
        raise ValueError("Unsupported file type. Please upload a .csv or .xlsx file.")

def validate_import_df(df: pd.DataFrame) -> list[str]:
    errors = []

    # missing required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    for col in missing:
        errors.append(f"Missing required column: **{col}**")

    if errors:
        return errors  # no point checking further if columns are missing

    # empty required fields
    for col in REQUIRED_COLUMNS:
        if df[col].isnull().any():
            count = df[col].isnull().sum()
            errors.append(f"**{col}** has {count} empty row(s) — all required fields must be filled.")

    # type checks
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

    # duplicate ItemIDs
    dupes = df["ItemID"].duplicated().sum()
    if dupes:
        errors.append(f"**ItemID** has {dupes} duplicate(s) — each item must have a unique ID.")

    return errors

def normalize_import_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "DateAdded" not in df.columns:
        df["DateAdded"] = datetime.today()
    df["DateAdded"] = pd.to_datetime(df["DateAdded"], errors="coerce")
    df["Quantity"]   = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    return df