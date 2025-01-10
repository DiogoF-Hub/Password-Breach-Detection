import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from main import start

start()

# Set up the page configuration
st.set_page_config(
    page_title="Password Breach Detection",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and subtitle
st.title("🔐 Password Breach Detection")
st.markdown(
    """
    ### Welcome to the Password Breach Detection Tool
    This tool helps you check if your password has been compromised in known data breaches. It also allows you to:
    - Search for a specific password in the database.
    - Download and manage the breached passwords database.
    - Analyze the most frequently seen passwords in breaches.
    - Add your own passwords to the database for testing purposes.

    **Currently using a 9GB database containing over 200 million SHA-1 hashed passwords!**

    The database is sourced from the [Have I Been Pwned](https://haveibeenpwned.com/) project and downloaded using tools provided by [Pwned Passwords Downloader](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader). It is hosted on my Google Drive for easy access.

    """
)

# Display a banner image (optional, if you have an image hosted online or locally)
# st.image("banner_image_url_or_path")

# Add buttons for navigation
st.markdown("#### What would you like to do?")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔍 Search Passwords"):
        # Example navigation logic
        switch_page("Search_Password")

with col2:
    if st.button("⬇️ Download DB"):
        # Example navigation logic
        switch_page("Download_DB")

with col3:
    if st.button("📊 Analyze Top Passwords"):
        # Example navigation logic
        switch_page("Analyze_Top_Passwords")

with col4:
    if st.button("➕ Add Passwords"):
        # Example navigation logic
        switch_page("Add_Passwords")

# Add a footer or additional details
st.markdown(
    """
    ---
    **About the Project**

    This project is developed as part of the first semester of the first year of the *BTS in Cybersecurity* program at **Lycée Guillaume Kroll**, Luxembourg (2024).

    [GitHub Repository](https://github.com/DiogoF-Hub/Password-Breach-Detection)

    """
)
