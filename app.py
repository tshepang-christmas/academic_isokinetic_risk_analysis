import streamlit as st

st.set_page_config(page_title="PHR 799", layout="wide")

st.image(r"C:\Users\user\Documents\GitHub\PHR_799\academic_isokinetic_risk_analysis\assets\a-i-r.png", use_container_width=True)

st.subheader("Enter Test Results")

with st.form("player_test_form"):
    player_id = st.text_input("Player ID")
    right_quad = st.number_input("Right Quadriceps Peak Torque (Nm)", min_value=0.0)
    right_ham = st.number_input("Right Hamstring Peak Torque (Nm)", min_value=0.0)
    left_quad = st.number_input("Left Quadriceps Peak Torque (Nm)", min_value=0.0)
    left_ham = st.number_input("Left Hamstring Peak Torque (Nm)", min_value=0.0)
    submitted = st.form_submit_button("Calculate")

if submitted:
    st.success(f"Received data for {player_id} — calculation logic not yet connected")