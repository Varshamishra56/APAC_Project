import streamlit as st
import pandas as pd
import os
from google.cloud import aiplatform  # Vertex AI Client

# Initialize Vertex AI
PROJECT_ID = os.getenv("GCP_PROJECT")
REGION = os.getenv("GCP_REGION")
aiplatform.init(project=PROJECT_ID, location=REGION)

# Placeholder Gemini API function for task prioritization (modify with real API)
def calculate_priority_score(vitals, lab_results, condition):
    # Hypothetical priority calculation, replace with actual Gemini API call
    return len(vitals) + len(lab_results) + (10 if condition == "Critical" else 5 if condition == "Serious" else 1)

# Sample patient data storage
patient_data = {
    "patient_id": [],
    "name": [],
    "age": [],
    "condition": [],
    "vitals": [],
    "lab_results": [],
    "priority_score": []
}

# Function to add a new patient task
def add_patient_task(patient_id, name, age, condition, vitals, lab_results):
    priority_score = calculate_priority_score(vitals, lab_results, condition)
    patient_data["patient_id"].append(patient_id)
    patient_data["name"].append(name)
    patient_data["age"].append(age)
    patient_data["condition"].append(condition)
    patient_data["vitals"].append(vitals)
    patient_data["lab_results"].append(lab_results)
    patient_data["priority_score"].append(priority_score)

# Streamlit UI
st.title("Healthcare Task Prioritization Assistant")

st.sidebar.header("Enter Patient Information")
patient_id = st.sidebar.text_input("Patient ID")
name = st.sidebar.text_input("Patient Name")
age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=30)
condition = st.sidebar.selectbox("Condition", ["Critical", "Serious", "Stable"])
vitals = st.sidebar.text_input("Vitals (e.g., BP, HR, Temp)")
lab_results = st.sidebar.text_input("Lab Results (e.g., WBC, Hemoglobin)")

if st.sidebar.button("Add Patient Task"):
    add_patient_task(patient_id, name, age, condition, vitals, lab_results)
    st.sidebar.success("Patient task added successfully!")

# Convert data to DataFrame for display
patient_df = pd.DataFrame(patient_data)
st.subheader("Task Prioritization")

# Display sorted tasks by priority score
if not patient_df.empty:
    sorted_df = patient_df.sort_values(by="priority_score", ascending=False)
    st.write(sorted_df)
else:
    st.write("No patient tasks added yet.")
