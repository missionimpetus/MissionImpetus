import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import StandardScaler

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load dataset function
def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    """
    logging.info(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

# Handle missing values by filling them with the mean (for numerical columns)
def handle_missing_values(df):
    """
    Fill missing values in the DataFrame with the column mean for numerical columns.
    """
    logging.info("Handling missing values...")
    for col in df.select_dtypes(include=np.number).columns:
        df[col].fillna(df[col].mean(), inplace=True)
    logging.info("Missing values handled successfully.")
    return df

# Remove duplicate rows
def remove_duplicates(df):
    """
    Remove duplicate rows from the DataFrame.
    """
    logging.info("Removing duplicate rows...")
    df.drop_duplicates(inplace=True)
    logging.info("Duplicate rows removed successfully.")
    return df

# Normalize numerical columns
def normalize_data(df):
    """
    Normalize numerical data columns using StandardScaler.
    """
    logging.info("Normalizing numerical data columns...")
    scaler = StandardScaler()
    numerical_cols = df.select_dtypes(include=np.number).columns
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    logging.info("Data normalized successfully.")
    return df

# Save the cleaned data to a new file
def save_cleaned_data(df, output_file):
    """
    Save the cleaned DataFrame to a new CSV file.
    """
    logging.info(f"Saving cleaned data to {output_file}...")
    df.to_csv(output_file, index=False)
    logging.info("Data saved successfully.")

# Main function to execute the entire cleaning process
def main():
    input_file = "data/raw_data.csv"  # Replace with your file path
    output_file = "data/cleaned_data.csv"
    
    # Load data
    df = load_data(input_file)
    if df is None:
        return

    # Clean data
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = normalize_data(df)

    # Save cleaned data
    save_cleaned_data(df, output_file)

if __name__ == "__main__":
    main()
