import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def create_target(df):
    """
    Create a binary target 'attended' based on whether 'Usage Time' is above the median.
    """
    threshold = df['Usage Time'].median()
    df['attended'] = (df['Usage Time'] > threshold).astype(int)
    return df

def train_model(df, features):
    """
    Train a RandomForestClassifier on the provided features and add predicted probabilities.
    Returns the trained model and the updated dataframe.
    """
    X = df[features]
    y = df['attended']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    # Add predicted probabilities to the dataframe
    df['attendance_prob'] = clf.predict_proba(X)[:, 1]
    
    return clf, df
