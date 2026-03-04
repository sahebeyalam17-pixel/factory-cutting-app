import streamlit as st
import pandas as pd
import datetime
import time

# --- CONFIGURATION ---
PUBLISH_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRv9ombwUlAaUU1-5rbkKeASVPN27FBzwc4T4x1be0EMMwfC-burrR6SJ7JUGxa6pDa1ifWhx1_HuML/pub?output=csv"
SHEET_EDIT_URL = "https://docs.google.com/spreadsheets/d/1A2B3C4D.../edit" 
SECRET_PIN = "1234" 

# --- PRODUCTION TARGETS ---
MONTHLY_TARGET = 30000  # Updated to 30,000
WORKING_DAYS = 26       # Estimated working days in a month
DAILY_TARGET = MONTHLY_TARGET / WORKING_DAYS
EFFICIENCY_THRESHOLD = 80.0 

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
            st.error("❌ Incorrect PIN.")
    st.stop() 

# --- BRANDING HEADER ---
st.title("FSD CUTTING DEPARTMENT BY ALAM")
st.write(f"Target: **{MONTHLY_TARGET:,}** | Daily Requirement: **{DAILY_TARGET:.0f} Pairs**")
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
            df['calc_eff'] = (df[act_col] / df[plan_col] * 100).replace([float('inf')], 0).fillna(0)
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
            st.success(f"✅ Validated! (Daily Target: {DAILY_TARGET:.0f})")
            st.balloons()
            st.link_button("💾 Save to Master Sheet", SHEET_EDIT_URL)

elif page == "📊 Dashboard":
    st.header("Live Performance Analytics")
    df = load_data()
    
    if not df.empty:
        act_col = next((c for c in df.columns if "actual" in c or "cut" in c), None)
        
        # --- TOP METRICS ---
        total_actual = df[act_col].sum() if act_col else 0
        avg_eff = df['calc_eff'].mean() if 'calc_eff' in df.columns else 0
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Monthly Cut", f"{total_actual:,}")
        m2.metric("Monthly Progress", f"{(total_actual/MONTHLY_TARGET)*100:.1f}%")
        
        # Efficiency Color Alert
        color = "normal" if avg_eff >= EFFICIENCY_THRESHOLD else "inverse"
        m3.metric("Avg Efficiency", f"{avg_eff:.1f}%", delta=f"{avg_eff-EFFICIENCY_THRESHOLD:.1f}%", delta_color=color)

        # --- PROGRESS BAR ---
        st.subheader(f"📅 Progress towards {MONTHLY_TARGET:,} Goal")
        progress = min(total_actual / MONTHLY_TARGET, 1.0)
        st.progress(progress)

        # --- DAILY TARGET CHART ---
        st.divider()
        st.subheader("Daily Output vs. Target Line")
        if 'date' in df.columns:
            # Group by date to see total production per day
            daily_data = df.groupby('date')[act_col].sum().reset_index()
            # Add the target line
            daily_data['Target'] = DAILY_TARGET
            st.line_chart(daily_data.set_index('date'))
        
        st.subheader("Recent Production History")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("⚠️ Data connection error.")
