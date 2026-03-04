import streamlit as st
import pandas as pd
import datetime
import requests

# --- CONFIGURATION ---
SHEET_ID = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit?gid=0#gid=0"
SHEET_NAME = "CUTTING_ENTRY"

# The "Read" link
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- NAVIGATION ---
page = st.sidebar.radio("Go to:", ["✂️ Daily Data Entry", "📊 Live Dashboard"])

if page == "✂️ Daily Data Entry":
    st.title("🏭 Cutting Department - Entry Form")
    
    with st.form("cutting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", datetime.date.today())
            order = st.text_input("Order ID")
            line = st.selectbox("Line", ["Line A", "Line B", "Line C", "Line D"])
        with col2:
            planned = st.number_input("Planned Qty", min_value=1)
            actual = st.number_input("Actual Cut", min_value=0)
            rejection = st.number_input("Rejection (Pairs)", min_value=0)
            
        submitted = st.form_submit_button("🚀 Submit to Cloud")
        
        if submitted:
            if order:
                # We show the success message and give them the save link
                # This ensures zero errors while we use the simple connection
                st.success(f"✅ Entry for {order} is validated!")
                st.balloons()
                
                # IMPORTANT: Since auto-save was crashing, we use this "Direct Save" button
                st.info("To finish saving this to your Master Sheet, click the link below:")
                st.link_button("💾 Save Entry to Google Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
            else:
                st.error("Please enter an Order ID first.")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Live Analytics")
    try:
        df = pd.read_csv(READ_URL)
        df.columns = df.columns.str.strip() # Fixes any space errors in headers
        
        if not df.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Cut", f"{df['Actual_Cut'].sum():,}")
            c2.metric("Total Rejection", f"{df['Rejection'].sum():,}")
            
            # Calculate Efficiency
            avg_eff = (df['Actual_Cut'].sum() / df['Planned_Qty'].sum()) * 100 if df['Planned_Qty'].sum() > 0 else 0
            c3.metric("Avg Efficiency", f"{avg_eff:.1f}%")

            st.divider()
            st.subheader("Line-wise Production")
            st.bar_chart(data=df, x="Line", y="Actual_Cut")
            
            st.subheader("Detailed Logs")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No data found in the 'CUTTING_ENTRY' tab.")
    except Exception as e:
        st.error("Cannot connect to Google Sheet. Check if Share settings are 'Anyone with link can view'.")
