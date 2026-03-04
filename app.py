import streamlit as st
import pandas as pd
import datetime
import time

# --- THE MASTER CONFIGURATION ---
# This is the ID from the link you just sent me
SHEET_ID = "1A2B3C4D..." 

# This link tells Google: "Give me the data as a CSV file right now"
DIRECT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- DATA LOADING ---
def load_data():
    try:
        # The 't' part at the end forces Google to give us fresh data every time
        df = pd.read_csv(f"{DIRECT_URL}&t={time.time()}")
        # This makes sure the app can read your headers even if they have spaces
        df.columns = [str(c).strip() for c in df.columns]
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
            rejection = st.number_input("Rejection (Pairs)", min_value=0)
            
        submitted = st.form_submit_button("🚀 Validate Data")
        
        if submitted:
            st.success(f"✅ Data for {order} is validated!")
            st.balloons()
            st.info("To finish saving, click the button below to open your Google Sheet:")
            st.link_button("💾 Save to Master Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Live Analytics")
    df = load_data()
    
    if not df.empty:
        # Display the table first so we know it's working
        st.subheader("Current Production Log")
        st.dataframe(df, use_container_width=True)
        
        # Look for the 'Actual_Cut' column to show the big number
        # We check both 'Actual_Cut' and 'Actual Cut' just in case
        actual_col = next((c for c in df.columns if "Actual" in c), None)
        rej_col = next((c for c in df.columns if "Rejection" in c), None)

        c1, c2 = st.columns(2)
        if actual_col:
            c1.metric("Total Pairs Cut", f"{df[actual_col].sum():,}")
            st.bar_chart(data=df, x="Line", y=actual_col)
        if rej_col:
            c2.metric("Total Rejections", f"{df[rej_col].sum():,}")
    else:
        st.error("⚠️ Dashboard is still not seeing your data.")
        st.write("---")
        st.subheader("Shabey, please check these 2 things in your Google Sheet:")
        st.write("1. **Is Row 1 empty?** (Delete any empty rows at the very top!)")
        st.write("2. **Are the headers in Row 1?** (Date, Order_ID, Line, Planned_Qty, Actual_Cut, Rejection)")
