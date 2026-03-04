import streamlit as st
import pandas as pd
import datetime
import time

# --- THE MASTER CONFIGURATION ---
# Replace only the letters/numbers between the quotes
SHEET_ID = "import streamlit as st
import pandas as pd
import datetime
import time

# --- THE MASTER CONFIGURATION ---
# Replace only the letters/numbers between the quotes
SHEET_ID = "1A2B3C4D..."

# This link tells Google: "Give me the data as a CSV file right now"
DIRECT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- DATA LOADING ---
def load_data():
    try:
        # The 't' part at the end forces Google to give us fresh data every time
        df = pd.read_csv(f"{DIRECT_URL}&t={time.time()}")
        # This makes sure the app can read your headers even if they have spaces
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
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
            st.success(f"✅ Data for {order} is ready!")
            st.link_button("💾 Save Entry to Master Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Live Analytics")
    df = load_data()
    
    if not df.empty:
        # Let's show the Raw Data first to make sure we see it
        st.subheader("Current Production Data")
        st.dataframe(df, use_container_width=True)
        
        # Then show the big numbers if the columns exist
        if "Actual_Cut" in df.columns:
            st.metric("Total Pairs Cut", f"{df['Actual_Cut'].sum():,}")
            st.bar_chart(data=df, x="Line", y="Actual_Cut")
    else:
        st.error("⚠️ The App cannot see your Google Sheet data yet.")
        st.write("### Follow these 2 steps to fix it:")
        st.write("1. **Share your Google Sheet:** Click 'Share' (top right) -> Set to 'Anyone with the link can view'.")
        st.write("2. **Add Data:** Make sure Row 1 of your sheet has these headers: `Date`, `Order_ID`, `Line`, `Planned_Qty`, `Actual_Cut`, `Rejection`.")"

# This link tells Google: "Give me the data as a CSV file right now"
DIRECT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- DATA LOADING ---
def load_data():
    try:
        # The 't' part at the end forces Google to give us fresh data every time
        df = pd.read_csv(f"{DIRECT_URL}&t={time.time()}")
        # This makes sure the app can read your headers even if they have spaces
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
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
            st.success(f"✅ Data for {order} is ready!")
            st.link_button("💾 Save Entry to Master Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Live Analytics")
    df = load_data()
    
    if not df.empty:
        # Let's show the Raw Data first to make sure we see it
        st.subheader("Current Production Data")
        st.dataframe(df, use_container_width=True)
        
        # Then show the big numbers if the columns exist
        if "Actual_Cut" in df.columns:
            st.metric("Total Pairs Cut", f"{df['Actual_Cut'].sum():,}")
            st.bar_chart(data=df, x="Line", y="Actual_Cut")
    else:
        st.error("⚠️ The App cannot see your Google Sheet data yet.")
        st.write("### Follow these 2 steps to fix it:")
        st.write("1. **Share your Google Sheet:** Click 'Share' (top right) -> Set to 'Anyone with the link can view'.")
        st.write("2. **Add Data:** Make sure Row 1 of your sheet has these headers: `Date`, `Order_ID`, `Line`, `Planned_Qty`, `Actual_Cut`, `Rejection`.")
