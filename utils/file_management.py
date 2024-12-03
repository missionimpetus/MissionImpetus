import os
import shutil
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rename a file
def rename_file(old_name, new_name):
    """
    Rename a file from old_name to new_name.
    """
    logging.info(f"Renaming file {old_name} to {new_name}...")
    try:
        os.rename(old_name, new_name)
        logging.info(f"File renamed successfully to {new_name}.")
    except FileNotFoundError:
        logging.error(f"File {old_name} not found.")
    except Exception as e:
        logging.error(f"Error renaming file: {e}")

# Move a file
def move_file(source, destination):
    """
    Move a file from source to destination.
    """
    logging.info(f"Moving file from {source} to {destination}...")
    try:
        shutil.move(source, destination)
        logging.info(f"File moved successfully.")
    except FileNotFoundError:
        logging.error(f"Source file {source} not found.")
    except Exception as e:
        logging.error(f"Error moving file: {e}")

# Copy a file
def copy_file(source, destination):
    """
    Copy a file from source to destination.
    """
    logging.info(f"Copying file from {source} to {destination}...")
    try:
        shutil.copy(source, destination)
        logging.info(f"File copied successfully.")
    except FileNotFoundError:
        logging.error(f"Source file {source} not found.")
    except Exception as e:
        logging.error(f"Error copying file: {e}")

# Delete a file
def delete_file(file_path):
    """
    Delete a file at the specified path.
    """
    logging.info(f"Deleting file {file_path}...")
    try:
        os.remove(file_path)
        logging.info(f"File deleted successfully.")
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
    except Exception as e:
        logging.error(f"Error deleting file: {e}")

# List files in a directory
def list_files_in_directory(directory):
    """
    List all files in the given directory.
    """
    logging.info(f"Listing files in directory {directory}...")
    try:
        files = os.listdir(directory)
        logging.info(f"Found {len(files)} files.")
        return files
    except FileNotFoundError:
        logging.error(f"Directory {directory} not found.")
        return []

# Main function
def main():
    directory = "./files"
    source = "source_file.txt"
    destination = "destination_file.txt"
    
    files = list_files_in_directory(directory)
    print(f"Files: {files}")
    
    # Demonstrating file management operations
    if source in files:
        rename_file(source, "new_name.txt")
        move_file("new_name.txt", destination)
        copy_file(destination, "backup.txt")
        delete_file("backup.txt")

if __name__ == "__main__":
    main()
