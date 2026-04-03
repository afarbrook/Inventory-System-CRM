import pandas as pd
from datetime import datetime, timedelta

"""
get_expiring_warranties(df, days) -- returns a DataFrame of items with expiring warranties
@param -- df is the inventory DataFrame, days is the number of days to check for expiring warranties
"""
def get_expiring_warranties(df: pd.DataFrame, days=30) -> pd.DataFrame:
    today = pd.Timestamp.today()
    threshold = today + pd.Timedelta(days=days)

    if "WarrantyExpiration" not in df.columns:
        return pd.DataFrame()

    df["WarrantyExpiration"] = pd.to_datetime(
        df["WarrantyExpiration"],
        errors="coerce"
    )

    expiring = df[df["WarrantyExpiration"] < threshold]
    expiring = expiring.sort_values("WarrantyExpiration")
    expiring["WarrantyExpiration"] = expiring["WarrantyExpiration"].dt.strftime("%m/%d/%Y")

    

    return expiring


