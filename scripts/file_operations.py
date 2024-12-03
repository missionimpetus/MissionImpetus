import os
import shutil
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a directory if it doesn't exist
def create_directory(directory):
    """
    Create a directory if it doesn't already exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directory '{directory}' created.")
    else:
        logging.info(f"Directory '{directory}' already exists.")

# List all files in a directory
def list_files(directory):
    """
    List all files in a given directory.
    """
    logging
