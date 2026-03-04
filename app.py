import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# 1. CONNECT TO GOOGLE SHEETS
# Replace the link below with your Google Sheet Share Link
# (Make sure the sheet is set to "Anyone with the link can Edit")
SQL_URL = "PASTE_YOUR_GOOGLE_SHEET_LINK_HERE"

conn = st.connection("gsheets", type=GSheetsConnection)

# --- NAVIGATION ---
page = st.sidebar.radio("Go to:", ["✂️ Daily Data Entry", "📊 Live Dashboard"])

if page == "✂️ Daily Data Entry":
    st.title("✂️ Cutting Entry (Cloud)")
    
    with st.form("cutting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("Date", datetime.date.today())
            order_id = st.text_input("Order ID")
            line = st.selectbox("Line", ["LINE A", "LINE B", "LINE C"])
        with col2:
            planned = st.number_input("Planned Qty", min_value=0)
            actual = st.number_input("Actual Cut", min_value=0)
            rejection = st.number_input("Rejection", min_value=0)
            
        submitted = st.form_submit_button("Submit to Cloud")
        
        if submitted:
            # Calculate and prepare data
            eff = round((actual / planned), 2) if planned > 0 else 0
            new_row = pd.DataFrame([{
                "Date": str(entry_date),
                "Order_ID": order_id.upper(),
                "Line": line,
                "Planned_Qty": planned,
                "Actual_Cut": actual,
                "Rejection": rejection,
                "Efficiency %": eff
            }])
            
            # Fetch existing data, append, and update Google Sheet
            existing_data = conn.read(spreadsheet=SQL_URL, worksheet="CUTTING_ENTRY")
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(spreadsheet=SQL_URL, worksheet="CUTTING_ENTRY", data=updated_df)
            st.success("✅ Data synced to Google Sheets!")

elif page == "📊 Live Dashboard":
    st.title("📊 Factory Live Dashboard")
    df = conn.read(spreadsheet=SQL_URL, worksheet="CUTTING_ENTRY")
    
    if not df.empty:
        # Metrics & Charts
        st.metric("Total Actual Cut (Cloud Total)", df["Actual_Cut"].sum())
        st.dataframe(df)
        st.bar_chart(df.set_index("Line")["Actual_Cut"])
    else:
        st.info("Waiting for cloud data...")
