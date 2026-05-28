import streamlit as st
import pandas as pd
from utils.importer import (
    load_uploaded_file,
    validate_import_df,
    normalize_import_df,
    import_df_to_supabase
)
from utils.excel import load_inventory

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

    errors = validate_import_df(import_df)

    if errors:
        st.error(f"❌ Your file is missing required column(s): {', '.join(f'`{c}`' for c in errors)}")
        st.stop()

    import_df = normalize_import_df(import_df)

    st.subheader("Preview Import")
    st.dataframe(import_df, use_container_width=True)

    # Filter out already-existing ItemIDs
    inventory_df = load_inventory()
    existing_ids = set(inventory_df["ItemID"])
    new_df = import_df[~import_df["ItemID"].isin(existing_ids)]
    skipped = len(import_df) - len(new_df)

    st.warning(f"This will add {len(new_df)} new items to the inventory.{f' ({skipped} duplicate IDs will be skipped.)' if skipped else ''}")

    if st.button("🚀 Import into Inventory"):
        if new_df.empty:
            st.error("No new items to import — all ItemIDs already exist in the inventory.")
        else:
            import_df_to_supabase(new_df)
            st.success(f"Imported {len(new_df)} new items successfully!")