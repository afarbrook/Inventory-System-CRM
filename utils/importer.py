import pandas as pd
from datetime import datetime

REQUIRED_COLUMNS = {
    "ItemID",
    "ItemName",
    "Category",
    "Quantity"
}

def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file, engine="openpyxl")
    else:
        raise ValueError("Unsupported file type")

def validate_import_df(df: pd.DataFrame) -> list[str]:
    missing = REQUIRED_COLUMNS - set(df.columns)
    return list(missing)

def normalize_import_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "DateAdded" not in df.columns:
        df["DateAdded"] = datetime.today()

    df["DateAdded"] = pd.to_datetime(df["DateAdded"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)

    return df
