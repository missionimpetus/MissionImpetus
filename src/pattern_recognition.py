import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.covariance import EllipticEnvelope
from sklearn.metrics import silhouette_score
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    """
    Load dataset from a CSV file.
    """
    logging.info(f"Loading data from {file_path}...")
    data = pd.read_csv(file_path)
    logging.info(f"Loaded dataset with {data.shape[0]} rows and {data.shape[1]} columns.")
    return data


def standardize_data(data):
    """
    Standardize the features of the data.
    """
    logging.info("Standardizing data...")
    scaler = StandardScaler()
    data_scaled = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    return data_scaled


def kmeans_clustering(data, n_clusters=3):
    """
    Perform K-means clustering on the data to identify patterns and group similar data points.
    """
    logging.info(f"Applying KMeans clustering with {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(data)
    logging.info(f"Cluster centers:\n{kmeans.cluster_centers_}")
    
    # Add cluster labels to data
    data['cluster'] = clusters
    
    # Calculate silhouette score to evaluate clustering quality
    silhouette = silhouette_score(data.drop('cluster', axis=1), clusters)
    logging.info(f"Silhouette score: {silhouette:.2f}")
    
    return data, kmeans


def plot_clusters(data, kmeans, pca_components=2):
    """
    Plot the data points and the clusters after performing PCA.
    """
    logging.info(f"Plotting clusters with {pca_components} principal components...")
    
    pca = PCA(n_components=pca_components)
    pca_data = pca.fit_transform(data.drop('cluster', axis=1))
    
    plt.figure(figsize=(10, 8))
    plt.scatter(pca_data[:, 0], pca_data[:, 1], c=data['cluster'], cmap='viridis', alpha=0.6)
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='red', marker='X')
    plt.title('KMeans Clustering with PCA Components')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.show()


def anomaly_detection(data):
    """
    Detect anomalies in the dataset using Elliptic Envelope method (robust to outliers).
    """
    logging.info("Performing anomaly detection using EllipticEnvelope...")
    envelope = EllipticEnvelope(contamination=0.05)
    anomalies = envelope.fit_predict(data)
    
    # -1 indicates anomalies, 1 indicates normal points
    data['anomaly'] = anomalies
    anomaly_data = data[data['anomaly'] == -1]
    
    logging.info(f"Number of detected anomalies: {anomaly_data.shape[0]}")
    return anomaly_data, data


def time_series_trend_analysis(data, date_column, value_column, window_size=7):
    """
    Analyze trends in a time-series dataset using a rolling window.
    """
    logging.info(f"Performing time-series trend analysis on {value_column}...")
    
    # Ensure the date column is in datetime format
    data[date_column] = pd.to_datetime(data[date_column])
    data.set_index(date_column, inplace=True)
    
    # Calculate rolling mean and standard deviation
    rolling_mean = data[value_column].rolling(window=window_size).mean()
    rolling_std = data[value_column].rolling(window=window_size).std()
    
    # Plot the trend with rolling statistics
    plt.figure(figsize=(12, 6))
    plt.plot(data[value_column], label=value_column, color='blue')
    plt.plot(rolling_mean, label='Rolling Mean', color='orange')
    plt.plot(rolling_std, label='Rolling Std Dev', color='green')
    plt.legend(loc='best')
    plt.title(f"Time-Series Trend Analysis: {value_column}")
    plt.show()
    
    return rolling_mean, rolling_std


def correlation_analysis(data):
    """
    Perform correlation analysis to identify patterns between features.
    """
    logging.info("Performing correlation analysis...")
    correlation_matrix = data.corr()
    
    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Feature Correlation Matrix')
    plt.show()
    
    return correlation_matrix


def z_score_outlier_detection(data, threshold=3):
    """
    Detect outliers using the Z-score method.
    """
    logging.info(f"Detecting outliers using Z-score with threshold {threshold}...")
    
    z_scores = np.abs(stats.zscore(data))
    outliers = (z_scores > threshold).any(axis=1)
    
    outlier_data = data[outliers]
    logging.info(f"Number of detected outliers: {outlier_data.shape[0]}")
    return outlier_data


def pattern_matching(data, pattern_column, threshold=0.7):
    """
    Identify patterns in a specific column using threshold-based pattern matching.
    """
    logging.info(f"Performing pattern matching in column {pattern_column}...")
    
    # Convert column values to strings and calculate similarity to the given pattern
    pattern = 'specific_pattern'  # Replace with the desired pattern
    data['pattern_match'] = data[pattern_column].apply(lambda x: int(pattern in str(x)))
    
    matched_data = data[data['pattern_match'] == 1]
    
    logging.info(f"Number of records matching pattern '{pattern}': {matched_data.shape[0]}")
    return matched_data


def detect_seasonality(data, date_column, value_column):
    """
    Detect seasonality in time series data using decomposition.
    """
    logging.info(f"Detecting seasonality for {value_column}...")
    
    # Convert the date column to datetime format
    data[date_column] = pd.to_datetime(data[date_column])
    
    # Perform seasonal decomposition
    from statsmodels.tsa.seasonal import seasonal_decompose
    decomposition = seasonal_decompose(data[value_column], model='additive', period=12)  # Monthly data
    
    # Plot the decomposition components
    decomposition.plot()
    plt.title(f"Seasonal Decomposition: {value_column}")
    plt.show()
    
    return decomposition


def main():
    # Load dataset
    data_path = 'data/raw/impetus_data.csv'
    data = load_data(data_path)
    
    # Standardize the data
    data_scaled = standardize_data(data)
    
    # Apply KMeans clustering
    data_with_clusters, kmeans_model = kmeans_clustering(data_scaled, n_clusters=3)
    plot_clusters(data_with_clusters, kmeans_model)
    
    # Detect anomalies
    anomalies, data_with_anomalies = anomaly_detection(data_scaled)
    
    # Time-series trend analysis
    date_column = 'date'  # Replace with your actual date column
    value_column = 'value'  # Replace with the actual value column
    rolling_mean, rolling_std = time_series_trend_analysis(data, date_column, value_column)
    
    # Correlation analysis
    correlation_matrix = correlation_analysis(data)
    
    # Z-score outlier detection
    outliers = z_score_outlier_detection(data_scaled)
    
    # Pattern matching
    matched_patterns = pattern_matching(data, 'behavior_column')
    
    # Detect seasonality
    seasonality_decomposition = detect_seasonality(data, date_column, value_column)


if __name__ == "__main__":
    main()
