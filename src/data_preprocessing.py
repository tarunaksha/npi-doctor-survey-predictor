import pandas as pd

def load_data(file_path):
    """
    Load the Excel file and return the main dataframe.
    Assumes the first sheet contains the primary dataset.
    """
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    return df

def preprocess_data(df):
    """
    Preprocess the dataframe:
    - Convert 'Login Time' and 'Logout Time' to datetime.
    - Ensure 'Usage Time' is numeric.
    - Extract 'login_hour' from 'Login Time'.
    
    The column definitions are:
      - NPI: Unique ID for the doctor.
      - State: Doctor's state.
      - Login Time: When the doctor logs in to the app.
      - Logout Time: When the doctor logs out of the app.
      - Usage Time: Active minutes in the app.
      - Region, Speciality, Count of Survey Attempts: Additional details.
    """
    df['Login Time'] = pd.to_datetime(df['Login Time'])
    df['Logout Time'] = pd.to_datetime(df['Logout Time'])
    
    # Ensure 'Usage Time' is numeric (active time in minutes)
    df['Usage Time'] = pd.to_numeric(df['Usage Time (mins)'], errors='coerce')
    
    # Extract the hour from the Login Time
    df['login_hour'] = df['Login Time'].dt.hour
    
    return df
