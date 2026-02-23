import pandas as pd

def generate_report(
    df: pd.DataFrame,
    category: str | None = None,
    low_stock_only: bool = False,
    start_date=None,
    end_date=None
) -> pd.DataFrame:
    report_df = df.copy()

    if category and category != "All":
        report_df = report_df[report_df["Category"] == category]

    if low_stock_only:
        report_df = report_df[report_df["Quantity"] < 5]

    if start_date:
        report_df = report_df[report_df["DateAdded"] >= pd.to_datetime(start_date)]

    if end_date:
        report_df = report_df[report_df["DateAdded"] <= pd.to_datetime(end_date)]

    return report_df.sort_values("DateAdded", ascending=False)
