import streamlit as st
from Utils.path_var import file_size_path, file_top10_path, file_passwords_temp


def clear_txt_files():
    files_to_clear = [file_size_path, file_top10_path, file_passwords_temp]

    try:
        for file in files_to_clear:
            # Open the file in write mode to clear its content
            with open(file, "w", encoding="utf-8") as f:
                pass  # Writing nothing clears the file

        st.success("✅ Cache files have been successfully cleared!")

    except Exception as e:
        st.error(f"❌ An error occurred while clearing files: {e}")
