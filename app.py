import streamlit as st
import pandas as pd
import datetime
import time

# --- CONFIGURATION ---
# Replace the ID below with the random letters/numbers from your browser URL
SHEET_ID = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit?gid=0#gid=0"

# This is the "Master Key" link that grabs the FIRST tab automatically
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- DATA LOADING ---
def load_data():
    try:
        # We add a timestamp so Google doesn't show "Old" data
        df = pd.read_csv(f"{READ_URL}&t={time.time()}")
        # Clean up column names (removes spaces/capitals)
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
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
            
        submitted = st.form_submit_button("🚀 Validate & Save")
        
        if submitted:
            st.success(f"✅ Data Validated!")
            st.link_button("💾 Save Entry to Google Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Live Analytics")
    df = load_data()
    
    if not df.empty:
        # Find the columns even if they have slightly different names
        # It will look for 'actual_cut' or 'actual' or 'qty'
        cols = df.columns.tolist()
        act_col = next((c for c in cols if "actual" in c or "cut" in c), None)
        rej_col = next((c for c in cols if "rej" in c), None)
        line_col = next((c for c in cols if "line" in c), None)

        c1, c2 = st.columns(2)
        if act_col:
            c1.metric("Total Pairs Cut", f"{df[act_col].sum():,}")
        if rej_col:
            c2.metric("Total Rejections", f"{df[rej_col].sum():,}")
        
        st.divider()
        if line_col and act_col:
            st.subheader("Production by Line")
            st.bar_chart(data=df, x=line_col, y=act_col)
        
        st.subheader("Master Data Log")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("⚠️ The Dashboard is not seeing any data.")
        st.write("---")
        st.subheader("Quick Check for Shabey:")
        st.write("1. Is your Google Sheet **TOTALLY EMPTY**? (Add one row of test data now!)")
        st.write("2. Are your headers in **Row 1**? (No titles above them!)")
        st.write("3. Is the first tab at the bottom of your sheet the one with the data?")
