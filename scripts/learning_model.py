import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load dataset
def load_data(file_path):
    """
    Load dataset from a CSV file.
    """
    logging.info(f"Loading dataset from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

# Preprocess data (handle missing values, encoding)
def preprocess_data(df):
    """
    Preprocess the dataset by handling missing values and encoding categorical variables.
    """
    logging.info("Preprocessing data...")
    
    # Handle missing values by filling with the mean for numerical columns
    df.fillna(df.mean(), inplace=True)
    
    # Encoding categorical columns if any
    df = pd.get_dummies(df, drop_first=True)
    logging.info("Data preprocessing completed.")
    return df

# Train a Logistic Regression model
def train_model(X_train, y_train):
    """
    Train a Logistic Regression model.
    """
    logging.info("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    logging.info("Model trained successfully.")
    return model

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model on the test set.
    """
    logging.info("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    logging.info(f"Accuracy: {accuracy}")
    logging.info(f"Classification Report:\n{report}")

# Main function to load data, preprocess, train, and evaluate the model
def main():
    input_file = "data/data.csv"  # Replace with your file path
    df = load_data(input_file)
    if df is None:
        return

    # Preprocess the data
    df = preprocess_data(df)
    
    # Split the data into features (X) and target (y)
    X = df.drop(columns=['target'])  # Replace 'target' with the actual target column name
    y = df['target']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()
