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

    **Currently, there are two database options available for download:**

    1. **OneDrive (Recommended):**
       - **Size:** ~9GB
       - **Entries:** ~200 million unique SHA-1 hashed passwords
       - **Link Valid Until:** *January 11, 2026*

    2. **PwnedPasswordsDownloader:**
       - **Size:** ~40GB
       - **Entries:** ~900 million unique SHA-1 hashed passwords
       - **Note:** The file must be named `pwnedpasswords.txt` and placed in the **root** of the project folder.
       - [Download from PwnedPasswordsDownloader](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader)

    The databases are sourced from the [Have I Been Pwned](https://haveibeenpwned.com/) project and made available for offline analysis.

    """
)

# Display a banner image (optional, if you have an image hosted online or locally)
# st.image("banner_image_url_or_path")

# Add buttons for navigation
st.markdown("#### What would you like to do?")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🔍 Search Passwords"):
        switch_page("Search_Password")

with col2:
    if st.button("📥 Download DB"):
        switch_page("Download_DB")

with col3:
    if st.button("📊 Analyze Top Passwords"):
        switch_page("Analyze_Top_Passwords")

with col4:
    if st.button("➕ Add Passwords"):
        switch_page("Add_Passwords")

with col5:
    if st.button("🗑️ Clear Cache"):
        switch_page("Clear_Cache")

# Add a footer or additional details
st.markdown(
    """
    ---
    **About the Project**

    This project is developed as part of the first semester of the first year of the *BTS in Cybersecurity* program at **Lycée Guillaume Kroll**, Luxembourg (2024).

    [GitHub Repository](https://github.com/DiogoF-Hub/Password-Breach-Detection)

    """
)
