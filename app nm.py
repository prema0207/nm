import streamlit as st
import pandas as pd
import time
import random

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("navigation_data.xlsx")

df = load_data()

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

# Streamlit UI
st.title("🤖 AI-EBPL – Autonomous Vehicles and Robotics")
st.markdown("""
This simulator demonstrates **autonomous decision-making** using sensor data and basic AI logic.  
Based on project documentation from **Phase 1 to 3**, this app simulates how an AI system processes distance data and makes real-time navigation decisions.
""")

if st.button("Start Simulation"):
    with st.spinner("Running Autonomous Navigation..."):
        robot = SmartAutonomousSystem(df)
        results = robot.run()
        for line in results:
            st.write(line)

# Optionally display raw data
with st.expander("📊 View Sensor Dataset"):
    st.dataframe(df)

with st.expander("📘 About This Project"):
    st.markdown("""
**AI-EBPL** stands for **Artificial Intelligence – Enhanced Behavior-based Perception Layer**.  
This project focuses on integrating:
- **Sensor fusion**
- **Real-time navigation**
- **AI-driven robotic task execution**
- **Secure deployment**

Developed for use cases in:
- Self-driving vehicles  
- Industrial automation  
- Healthcare robotics  
- Smart surveillance

For more, see project phases detailing [Problem Definition](#), [Innovation](#), and [Implementation](#).
""")
