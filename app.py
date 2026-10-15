# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db_handler import ClinicalDatabaseHandler
from datetime import datetime  
from calculation_engine import evaluate_isokinetic_profile

# --- Streamlit configuration execution first ---
st.set_page_config(page_title="PHR 799", layout="wide")

# --- 1. DYNAMIC CLIENT DATABASE SETUP ---
st.sidebar.title("📁 Client Database Manager")
client_name = st.sidebar.text_input("Active Client Namespace", value="default_squad").strip()

# Initialize your sharded database from db_handler.py
db = ClinicalDatabaseHandler(client_name)
st.sidebar.info(f"Connected to: `{db.db_filename}`")

# --- STREAMLIT UI LAYOUT ---
st.image(r"C:\Users\user\Documents\GitHub\PHR_799\academic_isokinetic_risk_analysis\assets\ARK.png", use_container_width=True)
st.subheader("Enter Test Results")
st.caption("Protocol: HUMAC NORM @ 60°/s | Framework: Croisier et al. (2008) Binary Model")

with st.form("player_test_form"):
    player_id = st.text_input("Player ID")
    dominant_leg = st.selectbox("Dominant Leg", options=["Right", "Left"])
    
    right_quad = st.number_input("Right Quadriceps Peak Torque (Nm)", min_value=0)
    right_ham = st.number_input("Right Hamstring Peak Torque (Nm)", min_value=0)
    left_quad = st.number_input("Left Quadriceps Peak Torque (Nm)", min_value=0)
    left_ham = st.number_input("Left Hamstring Peak Torque (Nm)", min_value=0)
    
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
        col1.metric("Dominant leg H:Q Ratio", f"{analysis['dom_hq']:.0f}%", help="Target: ≥ 80%")
        col2.metric("Non-Dominant H:Q Ratio", f"{analysis['ndom_hq']:.0f}%", help="Target: ≥ 80%")
        col3.metric("Bilateral Hamstring Asym.", f"{analysis['ham_asym']:.0f}%", help="Target: < 15%")

        if analysis["deficit_count"] > 0:
            st.warning("**Flagged risk factor deficits:**")
            for deficit in analysis["deficits"]:
                st.write(f"- {deficit}")

# --- INTERACTIVE VISUAL ANALYTICS DASHBOARD ---
st.markdown("---")
st.subheader("📊 Interactive Performance Analytics")

historical_df = db.load_records()

if not historical_df.empty:
    chart_df = historical_df.copy()
    chart_df["Hamstring Asymmetry (%)"] = chart_df["ham_asym"].round(0)
    chart_df["Dominant leg H:Q (%)"] = chart_df["dom_hq"].round(0)
    chart_df["Non-Dominant leg H:Q (%)"] = chart_df["ndom_hq"].round(0)
    
    fig = px.scatter(
        chart_df,
        x="Dominant leg H:Q (%)",
        y="Hamstring Asymmetry (%)",
        color="profile_status",
        color_discrete_map={"NORMAL PROFILE": "#2ecc71", "STRENGTH IMBALANCE PRESENT": "#e74c3c"},
        hover_name="player_id",
        hover_data={
            "timestamp": True,
            "Dominant leg H:Q (%)": ":.0f%",
            "Non-Dominant leg H:Q (%)": ":.0f%",
            "Hamstring Asymmetry (%)": ":.0f%"
        },
        title=f"Risk Profile Matrix for Workspace: '{client_name}'"
    )
    fig.add_vline(x=80.0, line_dash="dash", line_color="#7f8c8d", annotation_text="H:Q Threshold (80%)", annotation_position="top left")
    fig.add_hline(y=15.0, line_dash="dash", line_color="#7f8c8d", annotation_text="Asymmetry Threshold (15%)", annotation_position="top right")

     # 2. Deficit Area Shading Overlays (The Risk engine)
    # SHADE 1: Hamstring Asymmetry at 15% and ABOVE (Horizontal Red Block across the top)
    fig.add_hrect(y0=15.0, y1=100.0, fillcolor="#e74c3c", opacity=0.08, layer="below", line_width=0)
    
    # SHADE 2: Dominant H:Q BELOW 80% (Vertical Red Block down the left side)
    fig.add_vrect(x0=0.0, x1=80.0, fillcolor="#e74c3c", opacity=0.08, layer="below", line_width=0
    )

    # 3. Lock Visual Scales to keep the crosshair intersection perfectly centered
    fig.update_layout(
        xaxis_range=[20, 120],
        yaxis_range=[0, 50],
        plot_bgcolor="#f8f9fa"
    )

    st.plotly_chart(fig, use_container_width=True)

# --- HISTORICAL DATA LOGS ---
    st.markdown("### 📋 Historical Database Logs")
    st.dataframe(historical_df, use_container_width=True, hide_index=True)

    # --- ADMINISTRATIVE CONTROL PANEL ---
    st.markdown("#### ⚙️ Database Record Maintenance")
    admin_col1, admin_col2, admin_col3 = st.columns(3)
    
    with admin_col1:
        if st.button("🗑️ Rollback Latest Entry", key="btn_rollback", help="Permanently erases the most recently logged database row."):
            db.delete_last_entry()
            st.success("Latest record removed successfully.")
            st.rerun()
            
    with admin_col2:
        csv_backup = historical_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Workspace to CSV",
            data=csv_backup,
            file_name=f"backup_{client_name}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="btn_download_csv",
            help="Generates a localized csv file export backup."
        )
    with admin_col3:
        #Defensive check (Boundary value testing) to ensure the DataFrame is not empty before attempting to access unique player IDs
            if not historical_df.empty:
                unique_players = sorted(historical_df["player_id"].unique())
                selected_player = st.selectbox(
                "Select player's individual report 🔍", # MANDATORY LABEL: Always visible on screen
                options=unique_players,
                key="sb_history_lookup",
                help="Select a participant ID to audit their risk factor metrics" # HOVER INFO: Only pops up on mouse hover
                )
            if selected_player:
                player_history = historical_df[historical_df["player_id"] == selected_player]
                latest_evaluation_status = player_history.iloc[-1]
                st.markdown(f"**Latest Profile Status for {selected_player}**")
                st.caption("ℹ️Dominant and non-dominant H:Q ratios ≥ 80%; hamstring asymmetry < 15%."
                )

            if latest_evaluation_status["profile_status"] == "STRENGTH IMBALANCE PRESENT":
                st.error(f"⚠️ {latest_evaluation_status['profile_status']}")
                st.write(f"• Dominant H:Q Ratio: **{latest_evaluation_status['dom_hq']:.0f}%**")
                st.write(f"• Non-Dominant H:Q Ratio: **{latest_evaluation_status['ndom_hq']:.0f}%**")
                st.write(f"• Bilateral Hamstring Asymmetry: **{latest_evaluation_status['ham_asym']:.0f}%**")
                st.caption(f"📅 Last Screened: {latest_evaluation_status['timestamp']}"
                )

            else:
                st.success(f"✅ {latest_evaluation_status['profile_status']}")
                st.write(f"• Dominant H:Q Ratio: **{latest_evaluation_status['dom_hq']:.0f}%**")
                st.write(f"• Non-Dominant H:Q Ratio: **{latest_evaluation_status['ndom_hq']:.0f}%**")
                st.write(f"• Bilateral Hamstring Asymmetry: **{latest_evaluation_status['ham_asym']:.0f}%**")
                st.caption(f"📅 Last Screened: {latest_evaluation_status['timestamp']}"
                )