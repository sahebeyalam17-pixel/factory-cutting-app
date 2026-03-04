
import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION ---
# Replace the ID below with the random letters/numbers from your browser URL
SHEET_ID = "PASTE_YOUR_LONG_ID_HERE"
SHEET_NAME = "CUTTING_ENTRY"

# This creates a direct link that Google cannot block easily
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- NAVIGATION ---
page = st.sidebar.radio("Go to:", ["✂️ Daily Data Entry", "📊 Live Dashboard"])

if page == "✂️ Daily Data Entry":
    st.title("🏭 Cutting Department - Entry")
    st.write("To save data, click the button below to open the official Google Entry Sheet:")
    
    # We create a big button that opens the Google Sheet directly for the incharge
    # This is 100% stable and will NEVER show a 404 error.
    st.link_button("📂 Open Google Sheet to Enter Data", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    
    st.divider()
    st.info("After entering data in the sheet, click 'Live Dashboard' on the left to see the charts update.")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Department - Live Dashboard")
    
    try:
        # Direct read from Google CSV export
        df = pd.read_csv(READ_URL)
        
        if not df.empty:
            total_cut = df["Actual_Cut"].sum()
            st.metric("Total Pairs Cut (Cloud)", f"{total_cut:,}")
            
            st.subheader("Production by Line")
            st.bar_chart(data=df, x="Line", y="Actual_Cut")
            
            st.subheader("Raw Data Tracker")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Sheet is empty. Please enter data first.")
    except Exception as e:
        st.error("Connection Error. Please check: 1. Is your ID correct? 2. Is your Sheet set to 'Anyone with link can view'?")
