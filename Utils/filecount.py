import os
import streamlit as st
from Utils.path_var import file_path, file_size_path, file_passwords_temp


# This func loops the file to count the lines
def count_lines():
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            line_count = 0  # Initialize a counter
            for line in f:  # Iterate through each line in the file
                line_count += 1  # Increment the counter for each line
            return line_count
    except FileNotFoundError:
        # This except is not really needed bcs its already being check when the script runs but just in case
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error counting lines: {e}")


def write_cache(file_size_bytes, line_count):
    # Write the file size and line count to the cache.
    with open(file_size_path, "w", encoding="utf-8") as w:
        w.write(f"{file_size_bytes}:{line_count}\n")


# This is the func we call to get the lines bcs this one checks the temp too and if not calls the func above
def count_size_lines():
    try:
        # Get the current file size in bytes
        file_size_bytes = os.path.getsize(file_path)

        # Read the cache file
        with open(file_size_path, "r", encoding="utf-8") as r:
            first_line = r.readline().strip()
            if first_line:  # Cache is not empty
                Ar = first_line.split(":")
                file_size_bytes_saved = int(Ar[0])
                line_count_saved = int(Ar[1])

                # Check if the cached size matches the current size
                if file_size_bytes == file_size_bytes_saved:
                    # If yes just return the lines number saved
                    return line_count_saved

        # Bcs the cache did not match or was empty we call the func above to loop the file
        count_info = st.info(
            "Counting total lines in the file. This might take a few seconds..."
        )
        line_count = count_lines()
        count_info.empty()

        # Update the cache
        write_cache(file_size_bytes, line_count)

        return line_count

    except Exception as e:
        raise Exception(f"An error occurred: {e}")


# This func is used when we search for passwords, to know if we search in temp first or no
# Yes if the file is the same
# No if the file is not the same
def check_file_size_saved():
    file_size_bytes = os.path.getsize(file_path)
    with open(file_size_path, "r", encoding="utf-8") as r:
        first_line = r.readline().strip()
        if first_line:  # Cache is not empty
            Ar = first_line.split(":")
            file_size_bytes_saved = int(Ar[0])
            if file_size_bytes == file_size_bytes_saved:
                return True
            else:
                return False
        else:
            return False


# This func is called everytime we try to something with our db, and this checks if the db exists
def check_file_db():
    if os.path.exists(file_path):
        return True
    else:
        st.markdown("---")  # Another separator for cleaner layout

        st.error("❌ The `pwnedpasswords.txt` database is missing!")

        st.warning(
            "⚠️ Please download the required database to continue searching for compromised passwords.  \n"
            "➡️ To proceed go to the **Download DB** page to download the required database."
        )

        st.markdown("---")  # Another separator for cleaner layout
        return False


# This func is used to check passwords saved and check if the password is already there or no
def check_stored_passwords(sha1_hash):
    with open(file_passwords_temp, "r", encoding="utf-8") as f:
        for current_line in f:
            hash_temp, count, seen = current_line.strip().split(":")
            if hash_temp == sha1_hash:
                return current_line
    return False


# This one simply clears the stored passwords
def clear_stored_passwords():
    with open(file_passwords_temp, "w") as file:
        pass  # Writing nothing clears the file
