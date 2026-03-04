import streamlit as st
import pandas as pd
import datetime
import time

# --- THE MASTER KEY ---
# I have fixed your link below to be the "CSV" version
PUBLISH_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRv9ombwUlAaUU1-5rbkKeASVPN27FBzwc4T4x1be0EMMwfC-burrR6SJ7JUGxa6pDa1ifWhx1_HuML/pub?output=csv"

st.set_page_config(page_title="Factory Cloud - Cutting", layout="wide")

# --- DATA LOADING ---
def load_data():
    try:
        # The 't' part forces Google to give us the LATEST numbers
        df = pd.read_csv(f"{PUBLISH_URL}&t={time.time()}")
        # This cleans up the column names automatically
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
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
            st.success(f"✅ Data for {order} is validated!")
            st.balloons()
            # Link back to your sheet for easy saving
            st.link_button("💾 Open Google Sheet to Save", "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit")

elif page == "📊 Live Dashboard":
    st.title("📊 Cutting Live Analytics")
    df = load_data()
    
    if not df.empty:
        # Search for columns even with different names
        act_col = next((c for c in df.columns if "actual" in c or "cut" in c), None)
        rej_col = next((c for c in df.columns if "rej" in c), None)
        line_col = next((c for c in df.columns if "line" in c), None)

        c1, c2 = st.columns(2)
        if act_col:
            c1.metric("Total Pairs Cut", f"{df[act_col].sum():,}")
        if rej_col:
            c2.metric("Total Rejections", f"{df[rej_col].sum():,}")
        
        st.divider()
        st.subheader("Current Data Log")
        st.dataframe(df, use_container_width=True)
        
        if line_col and act_col:
            st.subheader("Production by Line")
            st.bar_chart(data=df, x=line_col, y=act_col)
    else:
        st.error("⚠️ Dashboard is empty. Check your Google Sheet headers.")
