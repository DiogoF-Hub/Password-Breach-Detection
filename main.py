import hashlib
import time
import os
import streamlit as st
from Utils.filecount import (
    count_size_lines,
    check_file_size_saved,
    check_file_db,
    check_stored_passwords,
    clear_stored_passwords,
)
from Utils.create_files_folders import create_folder, create_txt_files
from Utils.path_var import (
    current_folder,
    folder_path,
    file_path,
    file_size_path,
    file_top10_path,
    file_passwords_temp,
    bakfile,
    file_size_bytes_online,
)


# file_path = r"C:\Users\diogo\OneDrive - 365education\TxtFiles\pwnedpasswords.txt"


def start():
    if not os.path.exists(folder_path):
        create_folder(folder_path)

    if not os.path.exists(file_size_path):
        create_txt_files(file_size_path)

    if not os.path.exists(file_top10_path):
        create_txt_files(file_top10_path)

    if not os.path.exists(file_passwords_temp):
        create_txt_files(file_passwords_temp)

    if os.path.exists(bakfile):
        os.remove(bakfile)


def check_password_in_pwned(password):

    if check_file_db() == False:
        return

    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Check if the password was already searched and only if we have the sized stored
    if check_file_size_saved():
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

    total_lines = count_size_lines()

    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    progressNumber = st.empty()

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

                    # Write everything in one line and already inserts a new line for the next ones
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
                    status_placeholder.markdown(
                        f"**Elapsed Time:** {elapsed_time:.2f}s   \n"
                        f"**Estimated Remaining Time:** {(elapsed_time / current_line * total_lines) - elapsed_time:.2f}s"
                    )
                    progress_bar.progress(progress)
                    progressNumber.markdown(f"**Progress:** {progress * 100:.2f}%")

        elapsed_time = time.time() - start_time

        status_placeholder.empty()
        progress_bar.empty()
        progressNumber.empty()

        # Store the file not found
        line_to_write = f"{sha1_hash}:{0}:NotFound\n"
        with open(file_passwords_temp, "a") as file:
            file.write(line_to_write)

        error_placeholder = st.error(
            f"The password was not found in the list of breached passwords. Checked in {elapsed_time:.2f} seconds."
        )

    except Exception as e:
        error_placeholder = st.error(f"An error occurred: {e}")
