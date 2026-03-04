import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- IRONCLAD CONNECTION ---
# Replace the ID below with your long Google Sheet ID
SHEET_ID = "PASTE_YOUR_LONG_ID_HERE"
SHEET_NAME = "CUTTING_ENTRY"

# This creates a direct download link that Python can always read
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# --- NAVIGATION ---
page = st.sidebar.radio("Go to:", ["✂️ Daily Data Entry", "📊 Live Dashboard"])

def load_data():
    try:
        return pd.read_csv(GSHEET_URL)
    except:
        return pd.DataFrame(columns=['Date', 'Order_ID', 'Line', 'Planned_Qty', 'Actual_Cut', 'Rejection', 'Efficiency %'])

if page == "✂️ Daily Data Entry":
    st.title("✂️ Cutting Entry (Ironclad Mode)")
    
    with st.form("cutting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("Date", datetime.date.today())
            order_id = st.text_input("Order ID")
            line = st.selectbox("Line", ["LINE A", "LINE B", "LINE C"])
        with col2:
            planned = st.number_input("Planned Qty", min_value=1)
            actual = st.number_input("Actual Cut", min_value=0)
            rejection = st.number_input("Rejection", min_value=0)
            
        submitted = st.form_submit_button("Submit to Cloud")
        
        if submitted:
            st.info("To save data in Ironclad mode, simply copy this row to your Google Sheet, or stay tuned while we fix the auto-save!")
            # This version is for STABLE READING. 
            # If you want to WRITE, we must ensure your Google Sheet is 'Anyone with link can EDIT'
            st.write(f"New Data: {entry_date}, {order_id}, {actual} pairs.")

elif page == "📊 Live Dashboard":
    st.title("📊 Factory Live Dashboard")
    df = load_data()
    
    if not df.empty:
        st.metric("Total Actual Cut", df["Actual_Cut"].sum())
        st.dataframe(df, use_container_width=True)
        st.bar_chart(data=df, x="Line", y="Actual_Cut")
    else:
        st.warning("Could not find data. Please check your Google Sheet ID and Tab Name.")
