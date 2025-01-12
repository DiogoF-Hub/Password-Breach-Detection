import hashlib
import streamlit as st
from Utils.filecount import check_file_db
from Utils.path_var import file_path


def add_hash_to_file_end(password, count):

    if check_file_db(file_path) == False:
        return

    # Validation
    password = password.strip()
    if not password or not count or not isinstance(count, int):
        st.error("Invalid input: Password or count is missing/invalid.")
        return

    # Hash the password using SHA-1
    try:
        sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

        # Format the line as "<hash>:<count>"
        entry = f"{sha1_hash}:{count}\n"

        # Append to the file (at the end)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry)

        st.success(
            f"Password has been added successfully with hash {sha1_hash} and seen count {count}."
        )

    except Exception as e:
        st.error(f"An error occurred while adding the password: {e}")
