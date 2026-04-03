import pandas as pd

"""
generate_report(df, category, low_stock_only, start_date, end_date) -- generates a report based on the given criteria
@param -- df is the DataFrame containing the inventory data, category is the category to filter by, low_stock_only is a flag to include only low-stock items, start_date is the start date for filtering, end_date is the end date for filtering
@return -- a DataFrame containing the generated report
"""
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
