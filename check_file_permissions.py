import os
import stat

def check_file_permissions(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for name in dirs + files:
            file_path = os.path.join(root, name)
            file_permissions = os.stat(file_path).st_mode
            if not stat.S_ISDIR(file_permissions) and not stat.S_ISREG(file_permissions):
                print(f"Invalid file: {file_path}")
            else:
                print(f"File: {file_path}, Permissions: {file_permissions:o}")

# Example usage
folder_path = '/path/to/your/folder'
check_file_permissions(folder_path)
