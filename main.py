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


# This func will be ran when streamlit starts
# This creates the folder and the txt files inside
# And removes the bak file if it exists by any chance
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


# This is the func to loop the file and search for a password
def check_password_in_pwned(password):

    # Check if the db file exists before continuing
    if check_file_db() == False:
        return

    # .hexdigest converts that binary hash into a hexadecimal string, this makes it easier to read, store, or compare.
    # .upper will match the same way as its written in the file
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # This part we use to check if the password is stored in the temp passwords
    # Check if the password was already searched and only if we have the sized stored
    if check_file_size_saved():
        # Only check the password temp if the file size is saved and it matches the current one
        result = check_stored_passwords(sha1_hash)

        # If it finds something, this var will have something and if not the code will keep going
        if result:
            # split the string into different variables
            hash_in_file, count, seen = result.strip().split(":")

            # And here check if in the temp, the password has been seen=Found or not
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
        # If the file size is different from the one saved, delete whatever I have saved in this temp file
        clear_stored_passwords()

    total_lines = count_size_lines()

    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    progressNumber = st.empty()

    status_placeholder.info(f"Total lines in the file: {total_lines}\n")

    # Loop the file to check if the hash is there
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Current time to track the progress
            start_time = time.time()

            # Loop each line in the file
            for current_line, line in enumerate(f, start=1):
                # In case of a malformed line, just skip, but shouldnt happen
                try:
                    hash_in_file, count = line.strip().split(":")
                except ValueError:
                    status_placeholder.warning(
                        f"Skipping malformed line: {line.strip()}"
                    )
                    continue

                # If the hash in the current line is the same as the password hash, then I found it
                if hash_in_file == sha1_hash:
                    # Time now minus the time that it started i will get the time that it elapsed
                    elapsed_time = time.time() - start_time

                    # Here I save the current line in my cache but I add one more element equal to Found which means that the password has been seen
                    # Write everything in one line and already inserts a new line for the next ones
                    line = line.rstrip("\n") + ":Found\n"
                    with open(file_passwords_temp, "a") as file:
                        file.write(line)

                    result_placeholder = st.success(
                        f"The password has been seen {count} times in data breaches. Checked in {elapsed_time:.2f} seconds."
                    )
                    return

                # Update progress every 100000 lines
                # if the current line number is multiple of 100000 it will update
                # We do this so it doesnt update each line which makes python slower bcs of streamlit
                if current_line % 100000 == 0:
                    # Time now minus the time that it started i will get the time that it elapsed
                    elapsed_time = time.time() - start_time

                    # Streamlit progress bar is expecting a number from 0 to 1, where 0 is 0% and 1 is 100%
                    # This can be 0.1 or 0.7343, and this will be put into the bar
                    # min(progress_percentage, 1.0) ensures the value doesn't exceed 100%
                    progress = min(current_line / total_lines, 1.0)

                    # :.2f rounds the number to two decimal places and displays only those two digits after the decimal point.
                    status_placeholder.markdown(
                        f"**Elapsed Time:** {elapsed_time:.2f}s   \n"
                        f"**Estimated Remaining Time:** {(elapsed_time / current_line * total_lines) - elapsed_time:.2f}s"
                    )
                    progress_bar.progress(progress)
                    progressNumber.markdown(f"**Progress:** {progress * 100:.2f}%")

        # Time now minus the time that it started i will get the time that it elapsed
        elapsed_time = time.time() - start_time

        status_placeholder.empty()
        progress_bar.empty()
        progressNumber.empty()

        # Store the file not found
        # Here I save the current line in my cache but I add one more element equal to NotFound which means that the password has not been seen
        # Write everything in one line and already inserts a new line for the next ones
        line_to_write = f"{sha1_hash}:{0}:NotFound\n"
        with open(file_passwords_temp, "a") as file:
            file.write(line_to_write)

        error_placeholder = st.error(
            f"The password was not found in the list of breached passwords. Checked in {elapsed_time:.2f} seconds."
        )

    except Exception as e:
        error_placeholder = st.error(f"An error occurred: {e}")
