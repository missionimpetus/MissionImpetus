import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Plot histogram for a numerical column
def plot_histogram(df, column_name):
    """
    Plot a histogram for the specified numerical column.
    """
    if column_name not in df.columns:
        print(f"Column {column_name} not found in the dataset.")
        return
    
    plt.figure(figsize=(8, 6))
    sns.histplot(df[column_name], kde=True, color='blue')
    plt.title(f"Histogram of {column_name}")
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    plt.show()

# Plot a scatter plot between two numerical columns
def plot_scatter(df, col1, col2):
    """
    Plot a scatter plot between two numerical columns.
    """
    if col1 not in df.columns or col2 not in df.columns:
        print(f"Columns {col1} and/or {col2} not found in the dataset."
