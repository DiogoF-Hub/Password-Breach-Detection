import hashlib
import os
import sys

# Gets the absolute path of the current script
current_file_path = os.path.abspath(__file__)

# Moves up three levels in the directory hierarchy to reach the project root folder
project_root = os.path.abspath(os.path.join(current_file_path, "../../.."))

# Dynamically adds the project root to Python’s module search path
# Which makes all modules accessible as if the script were run from the project root
sys.path.append(project_root)

# We need the lines above so we can do these imports
from Utils.create_files_folders import create_folder
from Utils.get_pwnedpasswords_file import download_file


def add_hash_to_file(file_path):

    password = input("Enter the password you want to add: ")

    # while loop and try bcs the user might not type a number
    while True:
        try:
            count = int(
                input(
                    "Enter the number of times this password has been seen in breaches: "
                )
            )
            break
        except ValueError:
            print("Please enter a valid number.")

    # Hash the password using SHA-1
    # hexdigest is for converting to hexadecimal string and upper to match the other hashes inside the file
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Format the line as "<hash>:<count>"
    entry = f"{sha1_hash}:{count}\n"

    # Append to the file (at the end)
    try:
        # "a" append in the file
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"Added hash: {sha1_hash} with count {count} to the end of {file_path}")
    except Exception as e:
        print(f"Error: {e}")


# Gets the path of the current folder, which will be the root of the project bcs of the sys command above
current_folder = os.getcwd()

# creates the folder path by addind TxtFiles
txt_folder_path = os.path.join(current_folder, "TxtFiles")

# Check if the TxtFiles folder exists
if not os.path.exists(txt_folder_path):
    create_folder(txt_folder_path)
else:
    # Define the file name and full path
    file_name = "pwnedpasswords.txt"
    file_path = os.path.join(txt_folder_path, file_name)

    # Check if the file exists inside the TxtFiles folder
    if not os.path.exists(file_path):
        # If the file does not exist, download it
        download_file(file_path)

        # And finnally trigger the function to add files at the end
        add_hash_to_file(file_path)
    else:
        # If the file exists, just trigger the function
        add_hash_to_file(file_path)
