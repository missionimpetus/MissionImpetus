from ftplib import FTP

def connect_to_ftp(server, username, password):
    ftp = FTP(server)
    ftp.login(user=username, passwd=password)
    print(f"Connected to FTP server: {server}")
    return ftp

def list_files(ftp):
    print("Listing files:")
    ftp.retrlines('LIST')

def upload_file(ftp, file_path, remote_path):
    with open(file_path, 'rb') as f:
        ftp.storbinary(f"STOR {remote_path}", f)
        print(f"Uploaded {file_path} to {remote_path}")

def download_file(ftp, remote_path, local_path):
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f"RETR {remote_path}", f.write)
        print(f"Downloaded {remote_path} to {local_path}")

def disconnect_ftp(ftp):
    ftp.quit()
    print("Disconnected from FTP server.")

# Main function
if __name__ == "__main__":
    server = input("Enter FTP server: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    ftp = connect_to_ftp(server, username, password)
    list_files(ftp)

    action = input("Upload or download (u/d)? ").strip().lower()
    if action == 'u':
        local_file = input("Enter local file path: ")
        remote_file = input("Enter remote file path: ")
        upload_file(ftp, local_file, remote_file)
    elif action == 'd':
        remote_file = input("Enter remote file path: ")
        local_file = input("Enter local file path: ")
        download_file(ftp, remote_file, local_file)

    disconnect_ftp(ftp)
