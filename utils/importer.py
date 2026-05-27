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

        # single sheet — just read it
        if len(xl.sheet_names) == 1:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            return df.rename(columns=COLUMN_RENAMES)

        # two sheets — merge on ItemID
        sheet1 = xl.parse(xl.sheet_names[0])
        sheet2 = xl.parse(xl.sheet_names[1])

        # drop columns that exist in both to avoid _x/_y suffixes
        dupe_cols = [c for c in sheet2.columns if c in sheet1.columns and c != "ItemID"]
        sheet2 = sheet2.drop(columns=dupe_cols)

        merged = pd.merge(sheet1, sheet2, on="ItemID", how="outer")
        return merged.rename(columns=COLUMN_RENAMES)
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
    df["DateAdded"]  = pd.to_datetime(df["DateAdded"], errors="coerce")
    df["Quantity"]   = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    return df