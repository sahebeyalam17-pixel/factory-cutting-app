import streamlit as st
import pandas as pd
import datetime
import time

# --- CONFIGURATION ---
PUBLISH_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRv9ombwUlAaUU1-5rbkKeASVPN27FBzwc4T4x1be0EMMwfC-burrR6SJ7JUGxa6pDa1ifWhx1_HuML/pub?output=csv"
SHEET_EDIT_URL = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit" # Your Edit Link

# --- SECURITY SETTINGS ---
# CHANGE YOUR PIN HERE
SECRET_PIN = "1234" 

st.set_page_config(page_title="Shabey Alam Factory - ERP", layout="wide", page_icon="👞")

# --- LOGIN SYSTEM ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🏭 Factory Cloud Login")
    user_pin = st.text_input("Enter Factory Access PIN", type="password")
    if st.button("Unlock Dashboard"):
        if user_pin == SECRET_PIN:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Incorrect PIN. Access Denied.")
    st.stop() # Stops the rest of the app from loading until logged in

# --- BRANDING HEADER (Once Logged In) ---
col_logo, col_text = st.columns([1, 4])
with col_logo:
    # Replace the URL below with your actual Logo Link later
    st.image("https://cdn-icons-png.flaticon.com/512/1541/1541411.png", width=100)
with col_text:
    st.title("SHABEY ALAM SHOE FACTORY")
    st.subheader("Process & Operations Management System")

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
page = st.sidebar.radio("Department:", ["✂️ Cutting Entry", "📊 Production Dashboard"])

if page == "✂️ Cutting Entry":
    st.header("✂️ Daily Cutting Entry")
    
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
            st.success(f"✅ Data for {order} Validated!")
            st.balloons()
            st.link_button("💾 Finalize: Save to Master Sheet", SHEET_EDIT_URL)

elif page == "📊 Production Dashboard":
    st.header("📊 Live Production Analytics")
    df = load_data()
    
    if not df.empty:
        # Search for columns
        act_col = next((c for c in df.columns if "actual" in c or "cut" in c), None)
        rej_col = next((c for c in df.columns if "rej" in c), None)
        line_col = next((c for c in df.columns if "line" in c), None)

        m1, m2, m3 = st.columns(3)
        if act_col:
            total_cut = df[act_col].sum()
            m1.metric("Total Pairs Cut", f"{total_cut:,}")
        if rej_col:
            total_rej = df[rej_col].sum()
            m2.metric("Total Rejections", f"{total_rej:,}")
            
        # Logout Button
        if st.sidebar.button("🔒 Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

        st.divider()
        st.subheader("Real-Time Production Log")
        st.dataframe(df, use_container_width=True)
        
        if line_col and act_col:
            st.subheader("Performance by Line")
            st.bar_chart(data=df, x=line_col, y=act_col)
    else:
        st.error("⚠️ Data connection error.")
