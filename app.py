import streamlit as st
import pandas as pd
import datetime
import time

# --- CONFIGURATION ---
PUBLISH_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRv9ombwUlAaUU1-5rbkKeASVPN27FBzwc4T4x1be0EMMwfC-burrR6SJ7JUGxa6pDa1ifWhx1_HuML/pub?output=csv"
SHEET_EDIT_URL = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit" 
SECRET_PIN = "1234" 

# --- PRODUCTION TARGETS ---
MONTHLY_TARGET = 30000  # Change this to your actual monthly goal
EFFICIENCY_THRESHOLD = 80.0  # Red alert if below 80%

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
    st.write("Process & Operations Management | Visual Alerts & Goal Tracking")

st.divider()

# --- DATA LOADING ---
def load_data():
    try:
        df = pd.read_csv(f"{PUBLISH_URL}&t={time.time()}")
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        
        act_col = next((c for c in df.columns if "actual" in c or "cut" in c), None)
        plan_col = next((c for c in df.columns if "plan" in c), None)
        
        if act_col and plan_col:
            df[act_col] = pd.to_numeric(df[act_col], errors='coerce').fillna(0)
            df[plan_col] = pd.to_numeric(df[plan_col], errors='coerce').fillna(0)
            df['calc_eff'] = (df[act_col] / df[plan_col] * 100).replace([float('inf'), -float('inf')], 0).fillna(0)
        
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
            calc_eff = (actual / planned) * 100 if planned > 0 else 0
            st.success(f"✅ Data Validated! (Efficiency: {calc_eff:.1f}%)")
            st.balloons()
            st.link_button("💾 Save Entry to Master Sheet", SHEET_EDIT_URL)

elif page == "📊 Dashboard":
    st.header("Live Analytics & Targets")
    df = load_data()
    
    if not df.empty:
        act_col = next((c for c in df.columns if "actual" in c or "cut" in c), None)
        rej_col = next((c for c in df.columns if "rej" in c), None)

        m1, m2, m3 = st.columns(3)
        if act_col:
            total_actual = df[act_col].sum()
            m1.metric("Total Pairs Cut", f"{total_actual:,}")
            
            # --- COLOR CODED EFFICIENCY ---
            avg_eff = df['calc_eff'].mean()
            # Logic: If efficiency < 80, show red arrow down. If > 80, show green arrow up.
            delta_color = "normal" if avg_eff >= EFFICIENCY_THRESHOLD else "inverse"
            m3.metric(
                label="Avg Dept Efficiency", 
                value=f"{avg_eff:.1f}%", 
                delta=f"{avg_eff - EFFICIENCY_THRESHOLD:.1f}% vs Threshold",
                delta_color=delta_color
            )

        if rej_col:
            df[rej_col] = pd.to_numeric(df[rej_col], errors='coerce').fillna(0)
            total_rej = df[rej_col].sum()
            m2.metric("Total Rejections", f"{total_rej:,}", delta="- Good" if total_rej < 50 else "+ Critical", delta_color="inverse")

        # --- PROGRESS BAR FOR MONTHLY GOAL ---
        st.divider()
        st.subheader(f"📅 Monthly Production Goal: {MONTHLY_TARGET:,} Pairs")
        progress = min(total_actual / MONTHLY_TARGET, 1.0) # Cap at 100%
        st.progress(progress)
        st.write(f"**{total_actual:,}** pairs cut out of **{MONTHLY_TARGET:,}** target ({progress*100:.1f}%)")

        if st.sidebar.button("🔒 Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

        st.divider()
        st.subheader("Production Log")
        st.dataframe(df, use_container_width=True)
        
        if act_col:
            st.subheader("Performance Chart")
            st.bar_chart(data=df, x="line" if "line" in df.columns else df.columns[2], y=act_col)
    else:
        st.error("⚠️ Data connection error.")
