import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
import logging
import os
import re

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(data):
    """
    Clean the raw data by handling missing values, removing duplicates,
    and normalizing column names.
    """
    logging.info("Starting data cleaning process...")
    
    # Remove duplicate rows
    initial_shape = data.shape
    data = data.drop_duplicates()
    logging.info(f"Removed {initial_shape[0] - data.shape[0]} duplicates")
    
    # Normalize column names (lowercase and remove spaces)
    data.columns = [col.lower().replace(' ', '_') for col in data.columns]
    logging.info("Normalized column names.")
    
    # Handle missing values by replacing with NaN (if not already done)
    data.replace('NA', np.nan, inplace=True)
    return data


def impute_missing_values(data, strategy="mean"):
    """
    Impute missing values in the dataset using specified strategy (mean, median, most_frequent).
    """
    logging.info(f"Imputing missing values using {strategy} strategy...")
    
    imputer = SimpleImputer(strategy=strategy)
    imputed_data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)
    
    return imputed_data


def handle_categorical_columns(data):
    """
    Convert categorical columns to numerical representations using label encoding.
    """
    logging.info("Handling categorical columns...")
    
    categorical_columns = data.select_dtypes(include=['object']).columns
    label_encoder = LabelEncoder()
    
    for col in categorical_columns:
        if data[col].nunique() > 1:  # Skip columns with only one unique value
            logging.info(f"Label encoding column: {col}")
            data[col] = label_encoder.fit_transform(data[col].astype(str))
        else:
            logging.info(f"Skipping column: {col} (only one unique value)")
    
    return data


def remove_outliers(data, z_thresh=3):
    """
    Remove rows with outliers based on Z-score threshold for numerical columns.
    """
    logging.info("Removing outliers...")
    
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    z_scores = np.abs((data[numeric_columns] - data[numeric_columns].mean()) / data[numeric_columns].std())
    filtered_data = data[(z_scores < z_thresh).all(axis=1)]
    
    logging.info(f"Removed {data.shape[0] - filtered_data.shape[0]} outlier rows")
    return filtered_data


def feature_scaling(data):
    """
    Scale the features to a standard range using StandardScaler (mean=0, std=1).
    """
    logging.info("Scaling features...")
    
    scaler = StandardScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    
    return scaled_data


def split_data(data, target_column, test_size=0.2, random_state=42):
    """
    Split the data into train and test sets.
    """
    logging.info(f"Splitting data into train and test sets, with test size = {test_size}...")
    
    X = data.drop(target_column, axis=1)
    y = data[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    return X_train, X_test, y_train, y_test


def feature_engineering(data):
    """
    Create new features or transform existing features (e.g., creating interaction terms, binning).
    """
    logging.info("Starting feature engineering process...")
    
    # Example: Create new feature for age group (assuming there is an 'age' column)
    if 'age' in data.columns:
        data['age_group'] = pd.cut(data['age'], bins=[0, 18, 35, 50, 100], labels=['0-18', '19-35', '36-50', '51+'])
        logging.info("Created 'age_group' feature based on age.")
    
    # Example: Interaction term between 'income' and 'education'
    if 'income' in data.columns and 'education' in data.columns:
        data['income_education_interaction'] = data['income'] * data['education']
        logging.info("Created 'income_education_interaction' feature.")
    
    return data


def pca_dimensionality_reduction(data, n_components=2):
    """
    Reduce the dimensionality of the dataset using PCA.
    """
    logging.info(f"Applying PCA for dimensionality reduction to {n_components} components...")
    
    pca = PCA(n_components=n_components)
    pca_data = pca.fit_transform(data)
    
    pca_df = pd.DataFrame(pca_data, columns=[f"pca_{i+1}" for i in range(n_components)])
    
    logging.info(f"Reduced dimensions from {data.shape[1]} to {n_components}.")
    return pca_df


def feature_selection(data, target_column, k=10):
    """
    Select top k features based on univariate statistical tests (ANOVA F-test).
    """
    logging.info(f"Selecting top {k} features using ANOVA F-test...")
    
    X = data.drop(target_column, axis=1)
    y = data[target_column]
    
    selector = SelectKBest(f_classif, k=k)
    selector.fit(X, y)
    
    selected_features = X.columns[selector.get_support()]
    logging.info(f"Selected features: {selected_features}")
    
    return data[selected_features]


def remove_irrelevant_columns(data, columns_to_remove):
    """
    Remove irrelevant columns that are not useful for analysis (e.g., IDs, unimportant metadata).
    """
    logging.info(f"Removing irrelevant columns: {columns_to_remove}")
    
    data = data.drop(columns=columns_to_remove, axis=1, errors='ignore')
    
    return data


def preprocess_pipeline(data, target_column, outlier_threshold=3, pca_components=2, test_size=0.2):
    """
    Preprocess the dataset through the full pipeline: cleaning, imputation, scaling, splitting, etc.
    """
    logging.info("Starting full preprocessing pipeline...")
    
    # Clean the data
    data = clean_data(data)
    
    # Impute missing values
    data = impute_missing_values(data)
    
    # Handle categorical columns
    data = handle_categorical_columns(data)
    
    # Remove outliers
    data = remove_outliers(data, z_thresh=outlier_threshold)
    
    # Feature scaling
    data = feature_scaling(data)
    
    # Feature engineering
    data = feature_engineering(data)
    
    # Apply PCA for dimensionality reduction
    data_pca = pca_dimensionality_reduction(data, n_components=pca_components)
    
    # Feature selection
    data_selected = feature_selection(data, target_column, k=10)
    
    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = split_data(data_selected, target_column, test_size)
    
    return X_train, X_test, y_train, y_test, data_pca


if __name__ == "__main__":
    # Example usage
    data_path = 'data/raw/impetus_data.csv'
    data = pd.read_csv(data_path)
    
    # Run the full preprocessing pipeline
    target_column = 'target'  # Replace with your actual target column
    X_train, X_test, y_train, y_test, data_pca = preprocess_pipeline(data, target_column)
    
    logging.info("Preprocessing complete. Train and test sets ready.")
