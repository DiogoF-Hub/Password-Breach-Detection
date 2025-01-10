import hashlib
import time
import os
import streamlit as st
from Utils.filecount import count_size_lines, check_file_size_saved
from Utils.get_pwnedpasswords_file import download_file
from Utils.create_files_folders import create_folder, create_txt_files
from Utils.add_lines.add_end import add_hash_to_file_end
from Utils.add_lines.add_random import add_hash_to_random_line
from Utils.top_10_hashes import find_top_hashes


# Gets the path of the current folder
current_folder = os.getcwd()

# Full path of the folder to create
folder_path = os.path.join(current_folder, "TxtFiles")

# Define the txt files path
file_path = os.path.join(folder_path, "pwnedpasswords.txt")
file_size_path = os.path.join(folder_path, "fileSize.txt")
file_top10_path = os.path.join(folder_path, "fileTop10.txt")
file_passwords_temp = os.path.join(folder_path, "passwordsTemp.txt")


def start():
    if not os.path.exists(folder_path):
        create_folder(folder_path)

    if not os.path.exists(file_size_path):
        create_txt_files(file_size_path)

    if not os.path.exists(file_top10_path):
        create_txt_files(file_top10_path)

    if not os.path.exists(file_passwords_temp):
        create_txt_files(file_passwords_temp)


def check_file_db():
    if not os.path.exists(file_path):
        return False
    else:
        return True


def check_stored_passwords(sha1_hash):
    with open(file_passwords_temp, "r", encoding="utf-8") as f:
        for current_line in f:
            hash_temp, count, seen = current_line.strip().split(":")
            if hash_temp == sha1_hash:
                return current_line
    return False


def clear_stored_passwords():
    with open(file_passwords_temp, "w") as file:
        pass  # Writing nothing clears the file


def check_password_in_pwned(password):

    if check_file_db() == False:
        info_var = st.info("DB pwnedpasswords.txt is missing")
        if download_file(file_path) == False:
            return

    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Check if the password was already searched and only if we have the sized stored
    if check_file_size_saved(file_path, file_size_path):
        result = check_stored_passwords(sha1_hash)
        if result:
            hash_in_file, count, seen = result.strip().split(":")

            if seen == "Found":
                result_placeholder = st.success(
                    f"The password has already been seen {count} times in data breaches. Hashed taken from passwords that were already searched."
                )
                return
            else:
                error_placeholder = st.error(
                    f"The password was not found in the list of breached passwords. Checked in passwords already searched."
                )
                return
    else:
        # If the file size is different from the one saved, delete whatever I have saved in this temp
        clear_stored_passwords()

    total_lines = count_size_lines(file_path, file_size_path)

    status_placeholder = st.empty()
    progress_bar = st.progress(0)

    status_placeholder.info(f"Total lines in the file: {total_lines}\n")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            start_time = time.time()

            for current_line, line in enumerate(f, start=1):
                try:
                    hash_in_file, count = line.strip().split(":")
                except ValueError:
                    status_placeholder.warning(
                        f"Skipping malformed line: {line.strip()}"
                    )
                    continue

                if hash_in_file == sha1_hash:
                    elapsed_time = time.time() - start_time

                    line = line.rstrip("\n") + ":Found\n"
                    with open(file_passwords_temp, "a") as file:
                        file.write(line)

                    result_placeholder = st.success(
                        f"The password has been seen {count} times in data breaches. Checked in {elapsed_time:.2f} seconds."
                    )
                    return

                if current_line % 100000 == 0:
                    elapsed_time = time.time() - start_time
                    progress = min(current_line / total_lines, 1.0)
                    progress_bar.progress(progress)
                    status_placeholder.info(
                        f"Progress: {progress * 100:.2f}% | Elapsed Time: {elapsed_time:.2f}s | "
                        f"Estimated Remaining Time: {(elapsed_time / current_line * total_lines) - elapsed_time:.2f}s"
                    )

        elapsed_time = time.time() - start_time

        # Store the file not found
        line_to_write = f"{sha1_hash}:{0}:NotFound\n"
        with open(file_passwords_temp, "a") as file:
            file.write(line_to_write)

        error_placeholder = st.error(
            f"The password was not found in the list of breached passwords. Checked in {elapsed_time:.2f} seconds."
        )
        time.sleep(5)  # Wait for 5 seconds
        error_placeholder.empty()  # Clear the error message

    except Exception as e:
        error_placeholder = st.error(f"An error occurred: {e}")
        time.sleep(5)  # Wait for 5 seconds
        error_placeholder.empty()  # Clear the error message


"""
This part was when the code was running on terminal
"""


def loop_file():
    # Ask the user for a password
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
