import streamlit as st
import pandas as pd
import datetime
import time

# --- CONFIGURATION ---
PUBLISH_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRv9ombwUlAaUU1-5rbkKeASVPN27FBzwc4T4x1be0EMMwfC-burrR6SJ7JUGxa6pDa1ifWhx1_HuML/pub?output=csv"
SHEET_EDIT_URL = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit" 

# --- SECURITY SETTINGS ---
SECRET_PIN = "1234" 

st.set_page_config(page_title="FSD Cutting Dept", layout="wide", page_icon="✂️")

# --- LOGIN SYSTEM ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🏭 FSD Access Portal")
    user_pin = st.text_input("Enter Department PIN", type="password")
    if st.button("Unlock Dashboard"):
        if user_pin == SECRET_PIN:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Incorrect PIN. Access Denied.")
    st.stop() 

# --- BRANDING HEADER ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/1541/1541411.png", width=80)
with col_text:
    st.title("FSD CUTTING DEPARTMENT BY ALAM")
    st.write("Process & Operations Management | Efficiency & Production Tracking")

st.divider()

# --- DATA LOADING ---
def load_data():
    try:
        df = pd.read_csv(f"{PUBLISH_URL}&t={time.time()}")
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        return df
    except:
        return pd.DataFrame()

# --- NAVIGATION ---
page = st.sidebar.radio("Navigation:", ["✂️ Entry Form", "📊 Dashboard"])

if page == "✂️ Entry Form":
    st.header("Daily Production Entry")
    
    with st.form("cutting_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            date = st.date_input("Date", datetime.date.today())
            order = st.text_input("Order ID")
            line = st.selectbox("Line", ["Line A", "Line B", "Line C", "Line D"])
        with c2:
            planned = st.number_input("Planned Qty", min_value=1)
            actual = st.number_input("Actual Cut", min_value=0)
            rejection = st.number_input("Rejection", min_value=0)
            
        if st.form_submit_button("🚀 Validate & Save"):
            # Calculate efficiency for the success message
            calc_eff = (actual / planned) * 100 if planned > 0 else 0
            st.success(f"✅ Data for {order} Validated! (Efficiency: {calc_eff:.1f}%)")
            st.balloons()
            st.link_button("💾 Save Entry to Master Sheet", SHEET_EDIT_URL)

elif page == "📊 Dashboard":
    st.header("Live Analytics")
    df = load_data()
    
    if not df.empty:
        # Identify columns dynamically
        act_col = next((c for c in df.columns if "actual" in c or "cut" in c), None)
        rej_col = next((c for c in df.columns if "rej" in c), None)
        plan_col = next((c for c in df.columns if "plan" in c), None)
        # Look for efficiency specifically
        eff_col = next((c for c in df.columns if "eff" in c), None)

        m1, m2, m3 = st.columns(3)
        if act_col:
            m1.metric("Total Pairs Cut", f"{df[act_col].sum():,}")
        if rej_col:
            m2.metric("Total Rejections", f"{df[rej_col].sum():,}")
        
        # Calculate Average Efficiency from the data
        if act_col and plan_col:
            total_actual = df[act_col].sum()
            total_planned = df[plan_col].sum()
            avg_eff = (total_actual / total_planned) * 100 if total_planned > 0 else 0
            m3.metric("Avg Dept Efficiency", f"{avg_eff:.1f}%")

        if st.sidebar.button("🔒 Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

        st.divider()
        st.subheader("Production History (Includes Efficiency Column)")
        # This will now display all columns, including Column G (Efficiency)
        st.dataframe(df, use_container_width=True)
        
        if act_col:
            st.subheader("Performance Chart")
            st.bar_chart(data=df, x="line" if "line" in df.columns else df.columns[2], y=act_col)
    else:
        st.error("⚠️ Data connection error.")
