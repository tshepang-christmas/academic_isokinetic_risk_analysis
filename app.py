# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db_handler import ClinicalDatabaseHandler
from datetime import datetime  
from calculation_engine import evaluate_isokinetic_profile

# --- CRUCIAL FIX: Streamlit configuration MUST execute first ---
st.set_page_config(page_title="PHR 799", layout="wide")

# --- 1. DYNAMIC CLIENT DATABASE SETUP ---
st.sidebar.title("📁 Client Database Manager")
client_name = st.sidebar.text_input("Active Client Namespace", value="default_squad").strip()

# Initialize your sharded database from db_handler.py
db = ClinicalDatabaseHandler(client_name)
st.sidebar.info(f"Connected to: `{db.db_filename}`")

# --- STREAMLIT UI LAYOUT ---
st.image(r"C:\Users\user\Documents\GitHub\PHR_799\academic_isokinetic_risk_analysis\assets\a-i-r.png", use_container_width=True)
st.subheader("Enter Test Results")
st.caption("Protocol: HUMAC NORM @ 60°/s | Framework: Croisier et al. (2008) Binary Model")

with st.form("player_test_form"):
    player_id = st.text_input("Player ID")
    dominant_leg = st.selectbox("Dominant Leg", options=["Right", "Left"])
    
    right_quad = st.number_input("Right Quadriceps Peak Torque (Nm)", min_value=0.0)
    right_ham = st.number_input("Right Hamstring Peak Torque (Nm)", min_value=0.0)
    left_quad = st.number_input("Left Quadriceps Peak Torque (Nm)", min_value=0.0)
    left_ham = st.number_input("Left Hamstring Peak Torque (Nm)", min_value=0.0)
    
    save_option = st.selectbox(
        "Post-Calculation Action", 
        options=["Save to Database & Update Dashboard", "Run Calculation Only (Temp View)"]
    )
    
    submitted = st.form_submit_button("Calculate")

if submitted:
    if not player_id:
        st.error("Please enter a valid Player ID.")
    elif min(right_quad, right_ham, left_quad, left_ham) == 0:
        st.error("All peak torque metrics must be greater than 0 to evaluate deficits.")
    else:
        # Call the standalone calculation engine function
        analysis = evaluate_isokinetic_profile(dominant_leg, right_quad, right_ham, left_quad, left_ham)

        # Conditional database storage based on user choice
        if save_option == "Save to Database & Update Dashboard":
            try:
                db.save_record(player_id, dominant_leg, right_quad, right_ham, left_quad, left_ham, analysis)
                st.toast("✅ Record saved successfully to local database!")
            except Exception as e:
                st.error(f"Failed to log data to database: {e}")
        else:
            st.toast("ℹ️ Temporary calculation run. Data not committed.")

        # Display output results
        st.markdown("---")
        st.subheader(f"Diagnostic Profile: {player_id}")
        
        status_color = "red" if analysis["profile_status"] == "STRENGTH IMBALANCE PRESENT" else "green"
        st.markdown(
            f"<div style='padding:12px; border-radius:4px; background-color:{status_color}; color:white; "
            f"font-weight:bold; text-align:center; font-size:20px;'>{analysis['profile_status']}</div>", 
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Dominant H:Q Ratio", f"{analysis['dom_hq']:.1f}%", help="Target: ≥ 80%")
        col2.metric("Non-Dominant H:Q Ratio", f"{analysis['ndom_hq']:.1f}%", help="Target: ≥ 80%")
        col3.metric("Bilateral Hamstring Asym.", f"{analysis['ham_asym']:.1f}%", help="Target: < 15%")

        if analysis["deficit_count"] > 0:
            st.warning("**Flagged Clinical Deficits:**")
            for deficit in analysis["deficits"]:
                st.write(f"- {deficit}")