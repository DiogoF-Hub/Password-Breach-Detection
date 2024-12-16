import hashlib
import time
import os
from Utils.filecount import count_size_lines
from Utils.get_pwnedpasswords_file import download_file
from Utils.create_files_folders import create_folder, create_txt_files
from Utils.add_lines.add_end import add_hash_to_file_end
from Utils.add_lines.add_random import add_hash_to_random_line
from Utils.top_10_hashes import find_top_hashes


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
file_top10_path = os.path.join(current_folder, "TxtFiles", "fileTop10.txt")

"""
# Ensure the files exists before proceeding
if not os.path.exists(file_path):
    download_file(file_path)
"""

if not os.path.exists(file_size_path):
    create_txt_files(file_size_path)

if not os.path.exists(file_top10_path):
    create_txt_files(file_top10_path)


def check_file_db():
    if not os.path.exists(file_path):
        print("DB pwnedpasswords.txt is missing")
        download_file(file_path)


def check_password_in_pwned(password):
    print("\n")
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


def loop_file():
    # Ask the user for a password
    print("\n")
    user_password = input("Enter the password you want to check: ")

    # Check if the password exists in the file
    result = check_password_in_pwned(user_password)
    print(result)


def add_lines_switch():
    while True:
        try:
            print("\n")

            print("Which way would you like to add a line ?")
            print("1. At the end of file")
            print("2. Randomly inside the file")
            print("3. Go back")
            print("4. Exit")

            print("\n")

            user_input = int(input("Type the number of the action: "))

            if user_input not in range(1, 5):
                raise ValueError
        except ValueError:
            print("You must type a number between 1 and 4!")
        else:
            if user_input == 1:
                check_file_db()
                add_hash_to_file_end(file_path)
            elif user_input == 2:
                check_file_db()
                add_hash_to_random_line(file_path)
            elif user_input == 3:
                break
            else:
                exit()
            break

    start_func()


def get_top_switch():
    while True:
        try:
            print("\n")

            user_input = int(
                input("Enter the number of top hashes you want to find (e.g., 10): ")
            )
        except ValueError:
            print("You must type a number!")
        else:
            find_top_hashes(file_path, file_size_path, file_top10_path, user_input)
            break
    start_func()


def start_func():
    while True:
        try:
            print("\n")

            print("Which action would you like to do ?")
            print("1. Search for password inside the file")
            print("2. Download the DB pwnedpasswords.txt")
            print("3. Get the top most seen passwords from the DB pwnedpasswords.txt")
            print("4. Add passwords to DB pwnedpasswords.txt")
            print("5. Exit")

            print("\n")

            user_input = int(input("Type the number of the action: "))

            if user_input not in range(1, 6):
                raise ValueError
        except ValueError:
            print("You must type a number between 1 and 5!")
        else:

            if user_input == 1:
                check_file_db()
                loop_file()
            elif user_input == 2:
                download_file(file_path)
            elif user_input == 3:
                check_file_db()
                get_top_switch()
            elif user_input == 4:
                add_lines_switch()
            else:
                exit()


start_func()
