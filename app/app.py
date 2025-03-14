import streamlit as st
import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from src.data_preprocessing import load_data, preprocess_data
from src.model import create_target, train_model
from src.filter import filter_doctors_by_time

# Path to the dataset in the data folder
APP_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(APP_DIR, "..", "data", "dummy_npi_data.xlsx")
DATA_FILE = os.path.abspath(DATA_FILE)

# Load and preprocess data
df = load_data(DATA_FILE)
df = preprocess_data(df)
df = create_target(df)

# Define features to be used in the model.
# We use 'login_hour' (extracted from Login Time), 'Usage Time' (active minutes), and 'Count of Survey Attempts'
features = ['login_hour', 'Usage Time', 'Count of Survey Attempts']

# Train model and update dataframe with predicted attendance probabilities
model, df = train_model(df, features)

# Streamlit web app UI
st.title("NPI Doctor Survey Predictor")
st.write("Enter a survey time (e.g., 06:00) to get a list of doctors (NPIs) most likely to attend the survey.")

# Time input widget (default is 06:00)
input_time = st.time_input("Select Time:", datetime.time(6, 0))

if st.button("Find Doctors"):
    filtered_df = filter_doctors_by_time(df, input_time)
    if not filtered_df.empty:
        st.write("### Selected NPIs:")
        display_df = filtered_df[['NPI', 'attendance_prob']].copy()
        # Convert attendance probability from 0-1 to 0-100 and round to an integer
        display_df['attendance_prob'] = (display_df['attendance_prob'] * 100).round(0).astype(int)
        st.dataframe(display_df.rename(columns={'attendance_prob': 'Attendance Probability (%)'}))

        
        # Convert filtered data to CSV and offer download
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="selected_doctors.csv",
            mime="text/csv"
        )
    else:
        st.write("No doctors found matching the criteria. Please try a different time.")
