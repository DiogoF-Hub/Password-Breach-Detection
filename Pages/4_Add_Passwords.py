import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time
from Utils.add_lines.add_random import add_hash_to_random_line
from Utils.add_lines.add_end import add_hash_to_file_end

st.set_page_config(
    page_title="Add Passwords",
    page_icon="➕",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Title
st.title("➕ Add Passwords to the Database")

# Introduction
st.markdown(
    """
    Use this tool to add passwords to the database file:
    - You can manually add a single password at the **end** of the file or at a **random position**.
    """
)

# Manual password addition section
st.subheader("🔑 Add a Single Password")

# Input for the password
password_to_add = st.text_input(
    "Enter the password you want to add to the database:",
    placeholder="Type the password here...",
    type="password",
)

# Input for the "seen count"
seen_count = st.number_input(
    "Enter how many times this password has been seen:",
    min_value=1,
    value=1,
    step=1,
)

# Radio buttons for addition position
add_position = st.radio(
    "Where do you want to add this password?",
    options=[
        "At the end of the file",
        "At a random position (which might take some time)",
    ],
    index=0,
)

# Button to add the password
if st.button("Add Password"):
    password_stripped = password_to_add.strip()
    if password_stripped:
        if not isinstance(seen_count, int) or seen_count < 1:
            st.error("Please enter a number to add.")
        else:
            try:
                if add_position == "At the end of the file":
                    add_hash_to_file_end(password_stripped, seen_count)
                else:
                    add_hash_to_random_line(password_stripped, seen_count)
            except Exception as e:
                st.error(f"An error occurred while adding the password: {e}")
    else:
        st.error("Please enter a password to add.")

# Navigation back to home
if st.button("🏠 Go Back to Home"):
    switch_page("Home")
