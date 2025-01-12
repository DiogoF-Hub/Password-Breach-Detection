import streamlit as st
import time
import webbrowser
from streamlit_extras.switch_page_button import switch_page
from Utils.get_pwnedpasswords_file import download_file

st.set_page_config(
    page_title="Download DB",
    page_icon="📥",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------- Title Section ----------
st.title("📥  Download the Passwords Database")

# ---------- Description Section ----------
st.markdown(
    """
    **Welcome to the Download Page!**

    To search for compromised passwords, you need to download the latest version of the password database.

    If the database is already downloaded or incomplete, simply click "Download" again to delete the existing file and redownload it.

    Choose the best option for your needs below:
    """
)

st.markdown("---")

# ---------- Download Options Section ----------
st.subheader("Download Options")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Download from my OneDrive** (Recommended)")
    st.markdown("~9GB | ~200 million unique passwords")
    if st.button("⬇️ Download from my OneDrive"):
        download_file()

with col2:
    st.markdown("**Download from PwnedPasswordsDownloader**")
    st.markdown("~40GB | ~900 million unique passwords")
    if st.button("⬇️ Download from PwnedDownloader"):
        st.warning(
            "⚠️ Please ensure the file is named `pwnedpasswords.txt` and placed in the **root** of the project folder."
        )
        countdown_placeholder = st.empty()
        for i in range(5, 0, -1):
            countdown_placeholder.info(
                f"Redirecting to the PwnedDownloader page in {i} seconds..."
            )
            time.sleep(1)
        countdown_placeholder.empty()
        webbrowser.open_new_tab(
            "https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader"
        )

st.markdown("---")

# ---------- File Info Section ----------
st.subheader("📂 File Information")
st.markdown(
    """
    - **File Format:** SHA-1 hashes in plain text (`hash:count`)
    - **Count:** `count` represents how many times the password has been seen in known data breaches.
    - **Note:** Larger files provide more comprehensive breach coverage.
    """
)

st.markdown("---")

# ---------- Warning Section ----------
st.warning("⚠️ Please do not close this page during the download to avoid interruption.")

# ---------- Navigation Section ----------
if st.button("🏠 Go Back to Home"):
    switch_page("Home")
