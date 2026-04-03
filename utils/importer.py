import pandas as pd
from datetime import datetime

REQUIRED_COLUMNS = {
    "ItemID",
    "ItemName",
    "Category",
    "Quantity"
}

"""
load_uploaded_file(uploaded_file) -- loads the uploaded file into a DataFrame
@param -- uploaded_file is the file object to load
@return -- a DataFrame containing the file data
"""
def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file, engine="openpyxl")
    else:
        raise ValueError("Unsupported file type")

"""
validate_import_df(df) -- validates the imported DataFrame against required columns
@param -- df is the DataFrame to validate
@return -- a list of missing required columns
"""
def validate_import_df(df: pd.DataFrame) -> list[str]:
    missing = REQUIRED_COLUMNS - set(df.columns)
    return list(missing)

"""
normalize_import_df(df) -- normalizes the imported DataFrame
@param -- df is the DataFrame to normalize
@return -- a normalized DataFrame
"""
def normalize_import_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "DateAdded" not in df.columns:
        df["DateAdded"] = datetime.today()

    df["DateAdded"] = pd.to_datetime(df["DateAdded"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)

    return df
