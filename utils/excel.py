import pandas as pd
from pathlib import Path
from filelock import FileLock
import streamlit as st

INVENTORY_PATH = Path("data/Inventory.xlsx")
SHEET_NAME = "InventoryData"
LOCK_PATH = INVENTORY_PATH.with_suffix(".lock")

@st.cache_data
def _load_inventory(path: Path, last_modified: float) -> pd.DataFrame:
    df = pd.read_excel(
        path,
        sheet_name=SHEET_NAME,
        engine="openpyxl"
    )

    # Convert date columns properly
    df["DateAdded"] = pd.to_datetime(df["DateAdded"], errors="coerce")
    df["LastUpdated"] = pd.to_datetime(df["LastUpdated"], errors="coerce")
    df["WarrantyExpiration"] = pd.to_datetime(df["WarrantyExpiration"], errors="coerce")

    return df

def load_inventory() -> pd.DataFrame:
    if not INVENTORY_PATH.exists():
        return pd.DataFrame(columns=[
            "ItemID", "ItemName", "Category", "Quantity", "Location",
            "DateAdded", "LastUpdated", "Brand", "ModelNumber",
            "SerialNumber", "Cost", "Status",
            "WarrantyExpiration", "WarrantyProvider", "AlertSent"
        ])
    return _load_inventory(
        INVENTORY_PATH,
        INVENTORY_PATH.stat().st_mtime
    )
def save_inventory(df: pd.DataFrame):
    lock = FileLock(str(LOCK_PATH))
    with lock:
        df = df.copy()
        df["LastUpdated"] = pd.Timestamp.now()
        df.to_excel(
            INVENTORY_PATH,
            sheet_name=SHEET_NAME,
            index=False,
            engine="openpyxl"
        )

    # force reload everywhere
    st.cache_data.clear()
def append_inventory(existing: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat([existing, new], ignore_index=True)
    combined = combined.drop_duplicates(subset="ItemID", keep="last")
    return combined
