import streamlit as st
import pandas as pd
import time
import random

# UI Header
st.title("🤖 AI-EBPL – Autonomous Vehicles and Robotics")
st.markdown("""
This simulator demonstrates **autonomous decision-making** using sensor data and basic AI logic.  
Upload your dataset to simulate how an AI system processes distance data and makes real-time navigation decisions.
""")

# File uploader
uploaded_file = st.file_uploader("📤 Upload your `dataset.csv` file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Check required columns exist
        if 'sensor_id' not in df.columns or 'distance_cm' not in df.columns:
            st.error("The CSV file must contain `sensor_id` and `distance_cm` columns.")
        else:
            # Terrain classification logic
            def classify_terrain(distance_cm):
                return 'safe' if distance_cm >= 40 else 'unsafe'

            def ai_decision(terrain_class):
                return 'move_forward' if terrain_class == 'safe' else 'reroute'

            # Smart Autonomous System class
            class SmartAutonomousSystem:
                def __init__(self, data):
                    self.data = data
                    self.position = 0
                    self.log = []
                    self.safety_status = True

                def monitor_system(self):
                    if random.random() < 0.03:
                        self.safety_status = False
                        return False
                    return True

                def run(self):
                    log_output = []
                    for _, row in self.data.iterrows():
                        if not self.monitor_system():
                            log_output.append("[ALERT] System safety triggered! Halting operation.")
                            break

                        sensor_id = row["sensor_id"]
                        distance = row["distance_cm"]
                        terrain = classify_terrain(distance)
                        decision = ai_decision(terrain)

                        log_output.append(f"[Sensor {sensor_id}] Distance: {distance} cm -> {terrain.upper()} terrain")
                        log_output.append(f"[AI Decision] => {decision.replace('_', ' ').title()}\n")
                        self.log.append(decision)
                        time.sleep(0.1)

                    log_output.append(f">> Navigation Log: {self.log}")
                    log_output.append(f">> Status: {'COMPLETE' if self.safety_status else 'HALTED'}")
                    return log_output

            if st.button("🚗 Start Simulation"):
                with st.spinner("Running Autonomous Navigation..."):
                    robot = SmartAutonomousSystem(df)
                    results = robot.run()
                    for line in results:
                        st.write(line)

            with st.expander("📊 View Uploaded Sensor Data"):
                st.dataframe(df)

            with st.expander("📘 About This Project"):
                st.markdown("""
                **AI-EBPL** stands for **Artificial Intelligence – Enhanced Behavior-based Perception Layer**.  
                This project focuses on:
                - **Sensor fusion**
                - **Real-time navigation**
                - **AI-driven robotic task execution**
                - **Secure deployment**
                
                For self-driving vehicles, industrial automation, healthcare robotics, and smart surveillance.
                """)
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a `dataset.csv` file to begin.")
