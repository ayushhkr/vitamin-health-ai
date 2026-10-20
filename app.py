"""Streamlit interface for the trained Vitamin D model."""

from __future__ import annotations

import streamlit as st

from src.predict import load_metadata, load_model, predict_vitamin_d, vitamin_d_status


st.set_page_config(page_title="Vitamin D Predictor", page_icon="☀️", layout="centered")
st.title("Vitamin D Predictor")
st.caption("Educational estimate from the supplied custom dataset. It is not a clinical diagnosis.")

try:
    metadata = load_metadata()
    model = load_model()
except FileNotFoundError:
    st.error("Model files are missing. Run `python -m src.train` from the project folder first.")
    st.stop()

with st.form("prediction_form"):
    left, right = st.columns(2)
    with left:
        age = st.number_input("Age (years)", 1, 120, 25)
        gender = st.selectbox("Gender coding", options=[0, 1], help="Uses the dataset's original 0/1 coding.")
        weight = st.number_input("Weight (kg)", 20.0, 250.0, 70.0)
        height = st.number_input("Height (cm)", 80.0, 230.0, 170.0)
        body_fat = st.number_input("Body fat (%)", 1.0, 70.0, 22.0)
        sun = st.number_input("Sun exposure (minutes/day)", 0.0, 300.0, 25.0)
        skin_exposure = st.number_input("Skin exposure (%)", 0.0, 100.0, 40.0)
        sunscreen = st.selectbox("Sunscreen use", options=[0, 1])
    with right:
        alcohol = st.number_input("Alcohol (units/week)", 0.0, 50.0, 0.0)
        fish = st.number_input("Fish servings/week", 0.0, 30.0, 1.0)
        dairy = st.number_input("Dairy servings/week", 0.0, 30.0, 5.0)
        activity = st.number_input("Physical activity (hours/week)", 0.0, 80.0, 3.0)
        indoor = st.number_input("Indoor work (hours/day)", 0.0, 24.0, 7.0)
        skin_tone = st.selectbox("Skin tone coding", options=[1, 2, 3], help="Uses the dataset's original coding.")
    submitted = st.form_submit_button("Predict Vitamin D")

if submitted:
    bmi = weight / (height / 100) ** 2
    inputs = {
        "Age": age, "Gender": gender, "Weight_kg": weight, "Height_cm": height,
        "BMI": bmi, "BodyFat_percent": body_fat, "Sun_Exposure_min": sun,
        "Skin_Exposure_percent": skin_exposure, "Sunscreen_Use": sunscreen,
        "Alcohol_units_week": alcohol, "Fish_intake_week": fish, "Dairy_intake_week": dairy,
        "Physical_activity_hours_week": activity, "Indoor_work_hours_day": indoor,
        "Skin_tone": skin_tone,
    }
    prediction = predict_vitamin_d(inputs, model=model)
    st.metric("Predicted Vitamin D", f"{prediction:.1f} ng/mL")
    st.info(f"Estimated status: **{vitamin_d_status(prediction)}**")
    st.caption(metadata["data_label"])
