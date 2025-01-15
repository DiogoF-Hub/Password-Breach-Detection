import hashlib
import streamlit as st
from Utils.filecount import check_file_db
from Utils.path_var import file_path


def add_hash_to_file_end(password, count):

    # Check if the db file exists before continuing
    if check_file_db() == False:
        return

    # Validation
    password = password.strip()
    if not password or not count or not isinstance(count, int):
        st.error("Invalid input: Password or count is missing/invalid.")
        return

    # Hash the password using SHA-1
    try:
        # .hexdigest converts that binary hash into a hexadecimal string, this makes it easier to read, store, or compare.
        # .upper will match the same way as its written in the file
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
