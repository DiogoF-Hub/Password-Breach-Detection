import hashlib
import random
import fileinput
import os
import streamlit as st
from Utils.filecount import count_size_lines, check_file_db
from Utils.path_var import file_path, bakfile


def add_hash_to_random_line(password, count):
    add_warning = st.warning(
        "⚠️ Don't leave this page until this is done because you might break your local DB."
    )
    add_info = st.info("Adding the password...")
    progress_bar = st.empty()
    percentage_placeholder = st.empty()

    if check_file_db() == False:
        add_info.empty()
        add_warning.empty()
        return

    # Validation
    password = password.strip()
    if not password or not count or not isinstance(count, int) or count < 1:
        st.error("Invalid input: Password or count is missing/invalid.")
        add_info.empty()
        return

    try:
        # Generate SHA-1 hash of the password
        sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        line_to_insert = f"{sha1_hash}:{count}"

        total_lines = count_size_lines()
        random_line = random.randint(0, total_lines)

        progress_bar.progress(0)

        # Insert the line at the random position
        with fileinput.input(files=(file_path,), inplace=True, backup=".bak") as file:
            for current_line_number, line in enumerate(file):
                print(line, end="")

                if current_line_number == random_line:
                    print(line_to_insert)

                # Update progress every 100000 lines
                if (
                    current_line_number % 100000 == 0
                    or current_line_number == total_lines - 1
                ):
                    progress = (current_line_number + 1) / total_lines
                    progress_bar.progress(progress)
                    percentage_placeholder.markdown(
                        f"**Progress:** {progress * 100:.2f}%"
                    )

        if os.path.exists(bakfile):
            os.remove(bakfile)

        add_warning.empty()
        add_info.empty()
        progress_bar.empty()
        percentage_placeholder.empty()
        st.success(
            f"Password has been added successfully with hash {sha1_hash} and seen count {count} at a random position."
        )

    except Exception as e:
        add_info.empty()
        progress_bar.empty()
        st.error(f"An error occurred while adding the password: {e}")
