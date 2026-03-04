import streamlit as st
import pandas as pd
import datetime

# --- THE MASTER CONFIGURATION ---
# 1. Look at your Google Sheet URL. Copy the ID between /d/ and /edit
# Example: 1AbC_dEfGhIjKlMnOpQrStUvWxYz
SHEET_ID = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit?gid=0#gid=0"
SHEET_NAME = "CUTTING_ENTRY"

# This is the "Master Key" link - it asks Google for a CSV file directly
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- DATA LOADING ---
def load_data():
    try:
        # We add a 'cache' breaker to make sure it always gets the LATEST data
        import time
        df = pd.read_csv(f"{READ_URL}&cachebuster={time.time()}")
        df.columns = df.columns.str.strip() # Remove hidden spaces
        return df
    except Exception as e:
        return pd.DataFrame()

# --- NAVIGATION ---
page = st.sidebar.radio("Go to:", ["✂️ Daily Data Entry", "📊 Live Dashboard"])

if page == "✂️ Daily Data Entry":
    st.title("🏭 Cutting Department - Entry Form")
    st.info("Record production below. Once validated, you will save it to the Master Sheet.")
    
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
            
        submitted = st.form_submit_button("🚀 Validate & Save")
        
        if submitted:
            st.success(f"✅ Data for {order} is ready!")
            st.link_button("💾 Finalize: Save to Google Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Live Analytics")
    df = load_data()
    
    if not df.empty:
        # This part looks for your specific columns
        # If your columns are named 'Actual Cut' instead of 'Actual_Cut', it fixes it
        actual_col = "Actual_Cut" if "Actual_Cut" in df.columns else "Actual Cut"
        rej_col = "Rejection" if "Rejection" in df.columns else "Rejections"
        
        c1, c2 = st.columns(2)
        c1.metric("Total Pairs Cut", f"{df[actual_col].sum():,}")
        c2.metric("Total Rejections", f"{df[rej_col].sum():,}")
        
        st.divider()
        st.subheader("Production by Line")
        st.bar_chart(data=df, x="Line", y=actual_col)
        
        st.subheader("Master Data Log")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("⚠️ Dashboard is still empty.")
        st.write("1. Open your Google Sheet.")
        st.write("2. Click 'Share' -> Set to 'Anyone with link can VIEW'.")
        st.write(f"3. Ensure the first tab is your data.")
