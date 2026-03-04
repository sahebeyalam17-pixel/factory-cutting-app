import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- CONNECTION SETTINGS ---
# Replace this with your long ID from the browser URL
SHEET_ID = "PASTE_YOUR_LONG_ID_HERE"
SHEET_NAME = "CUTTING_ENTRY"

# This creates the link for the app to TALK to Google
SQL_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"

# Initialize the Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# --- NAVIGATION ---
page = st.sidebar.radio("Go to:", ["✂️ Daily Data Entry", "📊 Live Dashboard"])

if page == "✂️ Daily Data Entry":
    st.title("🏭 Cutting Department - Production Entry")
    
    with st.form("cutting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("Date", datetime.date.today())
            order_id = st.text_input("Order ID (e.g., ORD001)")
            line = st.selectbox("Line", ["LINE A", "LINE B", "LINE C", "LINE D"])
        with col2:
            planned = st.number_input("Planned Quantity (Pairs)", min_value=1)
            actual = st.number_input("Actual Cut (Pairs)", min_value=0)
            rejection = st.number_input("Rejections", min_value=0)
            
        submitted = st.form_submit_button("🚀 Submit Production Data")
        
        if submitted:
            if order_id:
                # Calculate Efficiency automatically
                eff = round((actual / planned), 2) if planned > 0 else 0
                
                # Prepare the new row
                new_row = pd.DataFrame([{
                    "Date": str(entry_date),
                    "Order_ID": order_id.upper(),
                    "Line": line,
                    "Planned_Qty": planned,
                    "Actual_Cut": actual,
                    "Rejection": rejection,
                    "Efficiency %": eff
                }])
                
                # READ existing data and APPEND the new row
                existing_data = conn.read(spreadsheet=SQL_URL, worksheet=SHEET_NAME)
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # SAVE back to Google Sheets
                conn.update(spreadsheet=SQL_URL, worksheet=SHEET_NAME, data=updated_df)
                st.success(f"✅ Successfully saved {actual} pairs for {order_id}!")
                st.balloons() # Just for fun!
            else:
                st.error("⚠️ Please enter an Order ID.")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Department - Live Dashboard")
    
    # Read the latest data from the Cloud
    df = conn.read(spreadsheet=SQL_URL, worksheet=SHEET_NAME)
    
    if not df.empty:
        # Show big numbers at the top
        total_cut = df["Actual_Cut"].sum()
        total_rej = df["Rejection"].sum()
        
        c1, c2 = st.columns(2)
        c1.metric("Total Pairs Cut", f"{total_cut:,}")
        c2.metric("Total Rejections", f"{total_rej:,}")
        
        st.divider()
        st.subheader("Production by Line")
        st.bar_chart(data=df, x="Line", y="Actual_Cut")
        
        st.divider()
        st.subheader("Raw Data Log")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data found. Please enter production data first.")
