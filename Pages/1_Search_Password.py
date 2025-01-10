import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from main import check_password_in_pwned

st.set_page_config(
    page_title="Search Password",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Title
st.title("🔍 Search for a Password in the Database")

# Introduction
st.markdown(
    """
    Use this tool to search if a specific password has been compromised in known breaches.

    This search is based on SHA-1 hashed passwords from a database containing over **200 million entries**.
    """
)

# Input field for the password
password = st.text_input("Enter the password you want to search for:", type="password")

# Placeholder for results
result_placeholder = st.empty()

# Button to search for the password
if st.button("Search"):
    if password.strip():
        info_var = st.info("Searching the database...")
        check_password_in_pwned(password)
        info_var.empty()
    else:
        st.error("Please enter a password to search.")

# Navigation back to home
if st.button("🏠 Go Back to Home"):
    switch_page("Home")
