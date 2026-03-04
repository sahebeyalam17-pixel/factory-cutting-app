import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION ---
# 1. PASTE YOUR LONG ID BETWEEN THE QUOTES BELOW
SHEET_ID = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit?gid=0#gid=0"
SHEET_NAME = "CUTTING_ENTRY"

# This link tells Google to send the data as a simple table
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- DATA LOADING ---
def load_data():
    try:
        # This line is the "Bridge" to your Google Sheet
        df = pd.read_csv(READ_URL)
        # Clean up column names (removes hidden spaces)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return pd.DataFrame()

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
            rejection = st.number_input("Rejection (Pairs)", min_value=0) # REJECTION IS BACK
            
        submitted = st.form_submit_button("Submit Production Data")
        
        if submitted:
            st.success("✅ Data Ready!")
            st.info("Click below to record this entry in the Master Google Sheet:")
            st.link_button("📂 Open Google Sheet to Save", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Live Analytics")
    df = load_data()
    
    if not df.empty:
        # Check if 'Actual_Cut' exists in your sheet
        if "Actual_Cut" in df.columns:
            total_cut = df["Actual_Cut"].sum()
            total_rej = df["Rejection"].sum() if "Rejection" in df.columns else 0
            
            c1, c2 = st.columns(2)
            c1.metric("Total Pairs Cut", f"{total_cut:,}")
            c2.metric("Total Rejections", f"{total_rej:,}")
            
            st.divider()
            st.subheader("Production by Line")
            st.bar_chart(data=df, x="Line", y="Actual_Cut")
            
            st.subheader("Master Data Log")
            st.dataframe(df, use_container_width=True)
        else:
            st.error("Column Name Mismatch! Make sure Row 1 of your Google Sheet has: Date, Order_ID, Line, Planned_Qty, Actual_Cut, Rejection")
    else:
        st.warning("No data found. Check your Spreadsheet ID and make sure the tab is named 'CUTTING_ENTRY'.")
