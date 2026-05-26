import streamlit as st
import pandas as pd
from utils.importer import (
    load_uploaded_file,
    validate_import_df,
    normalize_import_df
)
from utils.excel import save_inventory, load_inventory

if not st.session_state["logged in"]:
    st.error("Please log in.")
    st.stop()
st.set_page_config(page_title="Import Data", layout="wide")
st.header("📥 Bulk Import Inventory")

with st.expander("📋 Required & Optional Columns", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Required** ✅")
        st.markdown("""
        - `ItemID` — Unique identifier (e.g. ITM0001)
        - `ItemName` — Name of the item
        - `Category` — Type of item
        - `Quantity` — Number of units
        """)
    with col2:
        st.markdown("**Optional** _(leave blank if unknown)_")
        st.markdown("""
        - `Location` — Physical location
        - `AssignedTo` — Assigned employee
        - `Brand` / `ModelNumber` / `SerialNumber`
        - `Cost` — Purchase price
        - `Status` — e.g. Active, In Repair, Retired
        - `WarrantyExpiration` — Date (MM/DD/YYYY)
        - `WarrantyProvider` — Warranty contact
        """)

uploaded_file = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file:
    try:
        import_df = load_uploaded_file(uploaded_file)
    except Exception as e:
        st.error(str(e))
        st.stop()

    missing_cols = validate_import_df(import_df)

    if missing_cols:
        st.error(f"❌ Your file is missing required column(s): {', '.join(f'`{c}`' for c in missing_cols)}")
        st.stop()

    import_df = normalize_import_df(import_df)

    st.subheader("Preview Import")
    st.dataframe(import_df, use_container_width=True)

    st.warning(
        f"This will add {len(import_df)} items to the inventory."
    )

    if st.button("🚀 Import into Inventory"):
        inventory_df = load_inventory()

        # Prevent duplicate ItemID
        existing_ids = set(inventory_df["ItemID"])
        import_df = import_df[~import_df["ItemID"].isin(existing_ids)]

        combined = pd.concat(
            [inventory_df, import_df],
            ignore_index=True
        )

        save_inventory(combined)

        st.success(
            f"Imported {len(import_df)} new items successfully!"
        )
