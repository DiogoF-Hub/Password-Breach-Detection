import hashlib
import random
import fileinput
import os
import streamlit as st
from Utils.filecount import count_lines


def add_hash_to_random_line(file_path, password, count):
    # Validation
    password = password.strip()
    if not password or not count or not isinstance(count, int) or count < 1:
        st.error("Invalid input: Password or count is missing/invalid.")
        return

    try:
        # Generate SHA-1 hash of the password
        sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

        # Prepare the line to insert
        line_to_insert = f"{sha1_hash}:{count}"

        # Determine the total number of lines and pick a random line
        total_lines = count_lines(file_path)
        random_line = random.randint(0, total_lines)

        # Insert the line at the random position
        with fileinput.input(files=(file_path,), inplace=True, backup=".bak") as file:
            for current_line_number, line in enumerate(file):
                print(line, end="")  # Write existing lines
                if current_line_number == random_line:
                    print(line_to_insert)  # Insert the new line at the random position

        # Remove the backup file created during editing
        backup_file = file_path + ".bak"
        if os.path.exists(backup_file):
            os.remove(backup_file)

        success = st.success(
            f"Password has been added successfully with hash {sha1_hash} and seen count {count} at a random position."
        )

    except Exception as e:
        st.error(f"An error occurred while adding the password: {e}")


def add_hash_to_random_line_old(file_path):
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
        print("Attempting to insert the line randomly, this might take some seconds...")
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
