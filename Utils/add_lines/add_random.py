import hashlib
import random
import sys
import os

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


def add_hash_to_random_line(file_path):
    # Ask the user for a password
    password = input("Enter the password you want to add: ")

    # Ask the user for the number of times this password has been seen
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
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Format the line as "<hash>:<count>"
    entry = f"{sha1_hash}:{count}\n"

    try:
        # Read all lines from the file
        # This makes python load the file into the ram
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Generate a random position to insert the new entry
        random_position = random.randint(0, len(lines))

        # Insert the new entry at the random position
        lines.insert(random_position, entry)

        # Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(
            f"Added hash: {sha1_hash} with count {count} at line {random_position + 1} in {file_path}"
        )
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
        add_hash_to_random_line(file_path)
    else:
        # If the file exists, just trigger the function
        add_hash_to_random_line(file_path)
