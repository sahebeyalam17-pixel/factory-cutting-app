import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION ---
SHEET_ID = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit?gid=0#gid=0"
SHEET_NAME = "CUTTING_ENTRY"

# Direct URL for reading
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- NAVIGATION ---
page = st.sidebar.radio("Go to:", ["✂️ Daily Data Entry", "📊 Live Dashboard"])

def load_data():
    try:
        return pd.read_csv(READ_URL)
    except:
        return pd.DataFrame(columns=['Date', 'Order_ID', 'Line', 'Planned_Qty', 'Actual_Cut', 'Rejection'])

if page == "✂️ Daily Data Entry":
    st.title("🏭 Cutting Department Entry Form")
    
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", datetime.date.today())
            order = st.text_input("Order ID")
            line = st.selectbox("Line", ["Line A", "Line B", "Line C"])
        with col2:
            planned = st.number_input("Planned Qty", min_value=1)
            actual = st.number_input("Actual Cut", min_value=0)
            
        submitted = st.form_submit_button("Submit Production")
        
        if submitted:
            # Instead of crashing, we show the user exactly what to add
            st.success("✅ Data Ready for Cloud!")
            st.info("Since Google is blocking the direct auto-save, please click below to confirm this entry in the Master Sheet.")
            st.link_button("Confirm Entry in Google Sheets", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

elif page == "📊 Live Dashboard":
    st.title("📊 Live Production Dashboard")
    df = load_data()
    if not df.empty:
        st.metric("Total Actual Cut", df["Actual_Cut"].sum())
        st.bar_chart(data=df, x="Line", y="Actual_Cut")
        st.dataframe(df, use_container_width=True)
