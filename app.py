import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO
import datetime
import pandas as pd
import base64
import os

# ==========================================
# 1. PLATFORM CONFIGURATION & DESIGN
# ==========================================
st.set_page_config(
    page_title="Aegis Hospitality AI | Quality Assurance Dashboard", 
    page_icon="🏨", 
    layout="wide"
)

# Dark theme enterprise layout injection 
st.markdown("""
    <style>
    .main { background-color: #0f1116; }
    h1, h2, h3 { color: #f0f2f6 !important; font-family: 'Helvetica Neue', sans-serif; }
    div[data-testid="stMetricValue"] { font-size: 2.2rem; color: #4ade80; font-weight: 700; }
    .stButton>button { background-color: #1e293b; color: white; border: 1px solid #334155; }
    .stButton>button:hover { background-color: #3b82f6; border-color: #3b82f6; }
    </style>
""", unsafe_allow_html=True)

# Main Title Framework with Visual Brand Asset
title_col1, title_col2 = st.columns([0.85, 0.15])

with title_col1:
    st.title("🛡️ AEGIS HOSPITALITY AI")
    st.caption("Enterprise Multimodal Quality Assurance Autonomous Infrastructure v2.4")

with title_col2:
    # ----------------------------------------------------
    # COMPATIBLE FRONTEND IMAGE ASSET DECODING MATRIX (PNG)
    # ----------------------------------------------------
    base64_image_string = (
        "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwY"
        "AAACwUlEQVR4nO2Zy2sUURTGf9OkM0wzM8bYGEwUfCg+wE0gSgXduXChC0FwKfiAILgWwXWh"
        "In7gP0BwV90I7oUuXInSgAt9gIovfCg+wEw6bZpM0osZa6YzkzSdaZILfTAw3Mv5fR/n3HPP"
        "vYWhYWhoaGhoaGiY99A80AO8bOLeAn6m9G0P8Ag4bS6FNoDjwI9Un6W8pXbYyOAtYAnYDLwG"
        "noZ6w8AIUANuAk+AbaA7pE9SNoALId0R0F0U9oU9B9mHsk6gXf0T6I6gLw2UgfshbVfofofO"
        "AnpSujvYF/b9kK6v672mG6fR0Z9P6R5bH6u6pZDuDukN3XpI9yDkW8L+K91f1mcoZ6W7Eepu"
        "BDo9wBvAnT6OAnfS6T6A+0A3cBa4BNwBhoChpE8C1wOdB76ldI8An9Lp7gf39wX6wX1h3w/p"
        "+rpuxXWbofsdOgt8XmPfe90Z6G7SrepaXbcZuuPQ7Yfut+gG9AboIbpN0EfoPukT4f4FdAbo"
        "IfrDkL4P6O8H9PekfNid6A7RXYTuDdAjdOugT9DHQx8m8CHdfegToZ/vI9DDoIfoAnQH6Sbo"
        "PnQfegjdR7efboI+Qp+gT4Q+TOCb6B5A96F70EPoPrr9dBP0EfoEfYTuSfkI3SfdJ9D7wL3S"
        "fSrdO93D0r0v3Uu6V4HHwD3gLnCH7g66O8A94F5I9zBwW9idwG1hvwVsS+vWpXUtYMt667Xv"
        "te9XGgKGAc9H8DGlbwv7g0DfhbQz6O9Oun3gXsh3SfcK8Bi4l3QfSvcgdEfYrcDtUGe99bZ3"
        "6Wzvu+n6wW3X7YXuu+i2QbeFfhfQD7g+7fO+vS7X7bVunE6/A78X6CHdAeihkO4IdAfoAfoA"
        "3Yfuo9tPd5BuP/R66RXAfdp36Gzo9gHvhXQPpLsXujfUfU99w0RDQ0NDQ0NDQ0N98Bexn/oK"
        "f+w7+gAAAABJRU5ErkJggg=="
    )
    image_bytes = base64.b64decode(base64_image_string)
    st.image(image_bytes, output_format="PNG", use_container_width=True)

st.markdown("---")

# Initialize persistent session storage for the live tracking matrix table
if 'audit_history' not in st.session_state:
    st.session_state['audit_history'] = [
        {"Timestamp": "17:45:12", "Zone": "Room 102", "Metric": "94%", "Status": "PASS", "Action Taken": "Log Saved"},
        {"Timestamp": "18:02:44", "Zone": "Lobby Area", "Metric": "88%", "Status": "PASS", "Action Taken": "Log Saved"},
    ]
# ==========================================
# 2. MANAGEMENT CONTROL PANEL (SIDEBAR)
# ==========================================
st.sidebar.header("Control Panel")

# Variable validation sequence pulling keys invisibly from environment matrices
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif os.getenv("GEMINI_API_KEY"):
    api_key = os.getenv("GEMINI_API_KEY")
else:
    api_key = None

if api_key:
    st.sidebar.success("🔒 System Encryption Verified")
else:
    st.sidebar.error("❌ System Token Missing")

phone_ip = st.sidebar.text_input("Active Camera IP Core:", "10.182.93.231:8080")

st.sidebar.markdown("---")
st.sidebar.subheader("System Status")
st.sidebar.success("● AI Engine Core Operational")
st.sidebar.info("● RTSP Endpoint Synced")

if not api_key:
    st.error("⚠️ Enterprise Encryption Engine Missing. Please check your hosting provider deployment secrets settings.")
else:
    # Initialize credentials connection routing structures
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    stream_url = f"http://{phone_ip}/shot.jpg"

    # ==========================================
    # 3. HIGH-LEVEL KPI METRICS BAR
    # ==========================================
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Global Compliance Rating", value="91.2%", delta="+1.4%")
    m2.metric(label="Active Streams Monitored", value=f"{len(st.session_state['audit_history'])} Zones", delta="Live")
    m3.metric(label="Critical Infractions Flags", value="0", delta="0 Change", delta_color="inverse")
    m4.metric(label="Avg Turnaround Time", value="1.8s", delta="Optimal")
    st.markdown("---")

    # ==========================================
    # 4. OPERATIONS WORKSPACE LAYOUT
    # ==========================================
    left_pane, right_pane = st.columns(2)

    with left_pane:
        st.subheader("📹 Real-Time Video Ingestion")
        st.caption("Active monitoring array pulling data frames from designated resort zones.")
        
        # Zero-storage presentation mode toggle switch configuration
        demo_mode = st.toggle("✨ Enable Pitch Demo Presentation Mode (No Hardware Required)", value=True)
        
        # Action Buttons Layout
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            run_scan = st.button("🔄 Trigger Real-Time Patrol Scan", use_container_width=True)
        with btn_col2:
            clear_history = st.button("🗑️ Clear Audit Metrics Log", use_container_width=True)

        if clear_history:
            st.session_state['audit_history'] = []
            st.rerun()

        # Capture Sequence Execution
        if run_scan:
            if demo_mode:
                with st.spinner("Generating zero-storage synthetic hardware asset..."):
                    try:
                        # Dynamically creates a slate-blue layout canvas without using disk storage weight
                        live_image = Image.new('RGB', (500, 350), color='#1e293b')
                        st.image(live_image, caption="💡 Synthetic Presentation Matrix Asset Loaded", use_container_width=True)
                        st.session_state['current_patrol_img'] = live_image
                    except Exception as demo_err:
                        st.error(f"Matrix processor failure: {demo_err}")
            else:
                with st.spinner("Extracting active image frame from network stream node..."):
                    try:
                        response = requests.get(stream_url, timeout=6)
                        if response.status_code == 200:
                            live_image = Image.open(BytesIO(response.content))
                            st.image(live_image, caption="Secure Live Hardware Capture Frame", use_container_width=True)
                            st.session_state['current_patrol_img'] = live_image
                        else:
                            st.error(f"Hardware Ingestion Interrupted. Server Flag Code: {response.status_code}")
                    except Exception as e:
                        st.error(f"Network Timeout: Unable to query connection route. Trace: {e}")

    with right_pane:
        st.subheader("📋 Advanced AI Compliance Diagnostic Report")
        st.caption("Continuous model verification logic checking brand alignment metrics.")

        if run_scan and 'current_patrol_img' in st.session_state:
            with st.spinner("Executing cognitive matrix vision sweeps..."):
                prompt = """
                You are an expert Luxury Hotel Quality Assurance Director. Parse this live room feed.
                Deliver a highly meticulous, concise analysis exactly in this professional markdown layout:

                ### 🏛️ COMPLIANCE ASSESSMENT REPORT
                
                #### **📊 STRATEGIC PERFORMANCE SUMMARY**
                * **Tidiness & Presentation Score**: [Insert a score from 0% to 100%]
                * **Operational Verdict Status**: [Use text format: **PASS** or **CRITICAL DISCREPANCY**]
                * **Fault Department Designation**: [Housekeeping, Maintenance, Front Office, or None]
                
                #### **🔍 RECONNAISSANCE FINDINGS MATRIX**
                * Provide 2 to 3 punchy bullet points highlighting exact physical flaws (wrinkles, misalignments, clutter, loose wires) or confirm perfect execution.

                #### **🛠️ IMMEDIATE CORRECTIVE MANDATE DIRECTIVE**
                * Write exactly one highly specific physical command text string to assign directly to staff (e.g. "Re-press room center bedsheets to clear structural wrinkles immediately").
                """
                
                try:
                    ai_response = model.generate_content([prompt, st.session_state['current_patrol_img']])
                    output_text = ai_response.text
                    st.markdown(output_text)

                    # Append metrics seamlessly into historical log entries
                    status_flag = "FAIL" if "CRITICAL DISCREPANCY" in output_text else "PASS"
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    
                    new_log = {
                        "Timestamp": current_time,
                        "Zone": "Room 304 Feed (Demo)" if demo_mode else "Room 304 Live Feed",
                        "Metric": "Evaluated",
                        "Status": status_flag,
                        "Action Taken": "Supervisor Notified" if status_flag == "FAIL" else "Passed & Logged"
                    }
                    st.session_state['audit_history'].append(new_log)

                except Exception as ai_err:
                    st.error(f"AI Cognitive Framework Breakdown: {ai_err}")
        else:
            st.info("📊 Waiting for data frame ingestion pulse. Click the manual tracking trigger button to prompt diagnostic parsing metrics.")

    # ==========================================
    # 5. ENTERPRISE ACTIVITY LEDGER TABLE
    # ==========================================
    st.markdown("---")
    st.subheader("📜 Live Regional Operational Audit Logs")
    st.caption("Historical track ledger recording all continuous background events during current deployment cycle.")
    
    if st.session_state['audit_history']:
        df = pd.DataFrame(st.session_state['audit_history'])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("Ledger database layer is currently empty.")
