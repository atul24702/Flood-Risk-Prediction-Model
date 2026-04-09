import streamlit as st
import pickle
import numpy as np

# 1. Load the trained model
# Ensure 'flood_model.pkl' is in the same folder as this script
try:
    model = pickle.load(open("flood_model.pkl", "rb"))
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'flood_model.pkl' is in the directory.")

# 2. Set up the User Interface
st.title("🌊 Flood Risk Prediction System")
st.write("Enter the specific environmental details required by the model:")

# 3. Create 7 input fields to match the model's training data 
col1, col2 = st.columns(2)

with col1:
    monthly_rainfall = st.number_input("Monthly Rainfall (mm)", min_value=0.0)
    inundation_area = st.number_input("Inundation Area (sqm)", min_value=0.0)
    rainfall_7d = st.number_input("Rainfall in last 7 days (mm)", min_value=0.0)
    flood_count = st.number_input("Historical Flood Count", min_value=0)

with col2:
    river_dist = st.number_input("Distance to River (m)", min_value=0.0)
    infra_score = st.number_input("Infrastructure Score (0-10)", min_value=0.0, max_value=10.0)
    drainage_idx = st.number_input("Drainage Index (0-10)", min_value=0.0, max_value=10.0)

# 4. Prediction Logic
if st.button("Predict Flood Risk"):
    # The array must be in this exact order to match the model 
    input_data = np.array([[
        monthly_rainfall, 
        inundation_area, 
        rainfall_7d, 
        flood_count, 
        river_dist, 
        infra_score, 
        drainage_idx
    ]])
    
    # LinearRegression returns a continuous numerical prediction 
    prediction = model.predict(input_data)[0]

    st.divider()
    st.subheader(f"Prediction Score: {prediction:.2f}")

    # Threshold logic: Adjust the 0.5 value based on your specific project needs
    if prediction > 0.5:
        st.error("⚠️ Prediction: High Flood Risk")
    else:
        st.success("✅ Prediction: Low Flood Risk")

st.info("Note: This model uses Linear Regression. The output represents a risk score where higher values indicate greater flood probability.")