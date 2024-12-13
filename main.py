import hashlib
import time
import os
from Utils.filecount import count_size_lines
from Utils.get_pwnedpasswords_file import download_file
from Utils.create_files_folders import create_folder, create_txt_files


# Gets the path of the current folder
current_folder = os.getcwd()

# Full path of the folder to create
folder_name = "TxtFiles"
folder_path = os.path.join(current_folder, folder_name)
# Check if the folder exists
if not os.path.exists(folder_path):
    create_folder(folder_path)

# Define the txt files path
file_path = os.path.join(current_folder, "TxtFiles", "pwnedpasswords.txt")
file_size_path = os.path.join(current_folder, "TxtFiles", "fileSize.txt")


# Ensure the files exists before proceeding
if not os.path.exists(file_path):
    download_file(file_path)

if not os.path.exists(file_size_path):
    create_txt_files(file_size_path)


def check_password_in_pwned(password):
    # Calculate the SHA-1 hash of the password
    # hexdigest is for converting to hexadecimal string and upper to match the other hashes inside the file
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Count total lines in the file for progress tracking and wait 1s so the user can see the output
    total_lines = count_size_lines(file_path, file_size_path)
    print(f"Total lines in the file: {total_lines}\n")
    time.sleep(3)

    # Open the file and read line by line
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Get current time to count the time elapsed and remaining
            start_time = time.time()

            for current_line, line in enumerate(f, start=1):
                # Split the line into hash and count
                try:
                    line_splited = line.strip().split(":")
                    hash_in_file = line_splited[0]
                    count = line_splited[1]
                except ValueError:
                    print(f"Skipping malformed line: {line.strip()}")
                    continue

                # Compare the calculated hash with the hash from the file
                if hash_in_file == sha1_hash:
                    elapsed_time = time.time() - start_time
                    return f"The password has been seen {count} times in data breaches. Checked in {elapsed_time:.2f} seconds."

                # Progress tracking every 100,000 lines
                if current_line % 100000 == 0:
                    elapsed_time = time.time() - start_time
                    progress = (current_line / total_lines) * 100
                    estimated_total_time = (elapsed_time / current_line) * total_lines
                    estimated_remaining_time = estimated_total_time - elapsed_time
                    print(
                        f"Progress: {progress:.2f}% | Elapsed Time: {elapsed_time:.2f}s | Estimated Remaining Time: {estimated_remaining_time:.2f}s"
                    )

        # If the hash was not found
        elapsed_time = time.time() - start_time
        return f"The password was not found in the list of breached passwords. Checked in {elapsed_time:.2f} seconds."

    except Exception as e:
        return f"An error occurred: {e}"


# Ask the user for a password
user_password = input("Enter the password you want to check: ")

# Check if the password exists in the file
result = check_password_in_pwned(user_password)
print(result)
