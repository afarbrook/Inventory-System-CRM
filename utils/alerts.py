import pandas as pd
from datetime import datetime, timedelta


def get_expiring_warranties(df: pd.DataFrame, days=30):
    today = pd.Timestamp.today()
    threshold = today + pd.Timedelta(days)

    if "WarrantyExpiry" not in df.columns:
        return pd.DataFrame()

    df["WarrantyExpiry"] = pd.to_datetime(
        df["WarrantyExpiry"],
        errors="coerce"
    )

    return df[
        (df["WarrantyExpiry"].notna()) &
        (df["WarrantyExpiry"] <= threshold) &
        (df["WarrantyExpiry"] >= today)
    ]
