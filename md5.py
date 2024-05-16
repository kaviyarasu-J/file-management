import os
import hashlib
import time
import requests

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def monitor_folder(folder_path):
    file_hashes = {}
    file_hashes_new = {}

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_hashes[file_path] = calculate_md5(file_path)

    while True:
        # Update file_hashes_new to get the current state of the folder
        file_hashes_new.clear()
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                file_hashes_new[file_path] = calculate_md5(file_path)

        # Check for modified files
        for file_path in list(file_hashes.keys()):  # Create a copy of keys to iterate over
            if file_path not in file_hashes_new:
                print(f"File {file_path} deleted!")
                requests.post("https://ntfy.sh/files",
                              data="File deleted: {}".format(file_path).encode(encoding='utf-8'))
                del file_hashes[file_path]
            elif file_hashes[file_path] != file_hashes_new[file_path]:
                print(f"File {file_path} modified!")
                requests.post("https://ntfy.sh/files",
                              data="File modified: {}".format(file_path).encode(encoding='utf-8'))
                file_hashes[file_path] = file_hashes_new[file_path]

        # Check for newly added files
        for file_path in file_hashes_new.keys():
            if file_path not in file_hashes:
                print(f"File {file_path} added!")
                requests.post("https://ntfy.sh/files",
                              data="File added: {}".format(file_path).encode(encoding='utf-8'))
                file_hashes[file_path] = file_hashes_new[file_path]

        # Sleep for some time before the next iteration
        time.sleep(2)

folder_path = "C:/Users/Admin/OneDrive/Desktop/pravartak"
monitor_folder(folder_path)
