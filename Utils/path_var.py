import os

"""
In this file I define all the file path to be used in every other func
"""

# Gets the path of the current folder
current_folder = os.getcwd()

# Full path of the folder to create
folder_path = os.path.join(current_folder, "TxtFiles")

# Define the txt files path
file_path = os.path.join(current_folder, "pwnedpasswords.txt")

bakfile = os.path.join(current_folder, "pwnedpasswords.txt.bak")

# Temp Files
file_size_path = os.path.join(folder_path, "fileSize.txt")
file_top10_path = os.path.join(folder_path, "fileTop10.txt")
file_passwords_temp = os.path.join(folder_path, "passwordsTemp.txt")

# Expected File size in bytes (8.39 GB)
# _ are only used for readability and does not affect the value of the number.
file_size_bytes_online = 9_010_985_310
