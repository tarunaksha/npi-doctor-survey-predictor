import pandas as pd

def save_dataframe_to_csv(df, file_name):
    """
    Save the dataframe to a CSV file.
    """
    df.to_csv(file_name, index=False)
