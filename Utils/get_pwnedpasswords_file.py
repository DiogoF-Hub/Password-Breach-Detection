import requests
from requests.exceptions import RequestException
import streamlit as st
import os
from Utils.path_var import file_path, file_size_bytes_online, bakfile


# Url to download the txt file with the hashes
# This url will work until the 11 of January of 2026
# The url has been modified from :t: to :u: so it forces a direct download and added &download=1 which forces browser/requests to download the file instead of opening it
url = "https://365education-my.sharepoint.com/:u:/g/personal/cardi782_school_lu/Ednvv2j9VOpCqjZEsZ4ZhcEB4xqK9sSGlIQKG_Izh8aYfg?e=6XfJOY&download=1"


def download_file():

    info_var = st.empty()
    status_placeholder = st.empty()
    progress_bar = st.empty()

    if os.path.exists(file_path):
        if file_size_bytes_online != os.path.getsize(file_path):
            os.remove(file_path)
            if os.path.exists(bakfile):
                os.remove(bakfile)
        else:
            status_placeholder.success(f"✅ File already exists: {file_path}")
            return

    try:
        progress_bar.progress(0)
        info_var.info(f"Downloading to {file_path}")

        # Attempt to connect to the URL
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Open file in binary write mode
        with open(file_path, "wb") as file:
            chunk_size = 5 * 1024 * 1024  # 5MB chunks
            downloaded = 0

            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)
                    downloaded += len(chunk)

                    # Update progress in Streamlit
                    progress_percentage = downloaded / file_size_bytes_online
                    progress_bar.progress(min(progress_percentage, 1.0))  # Cap at 100%

                    status_placeholder.info(
                        f"Downloaded: {downloaded / (1024 * 1024):.2f} MB / {file_size_bytes_online / (1024 * 1024):.2f} MB  \n"
                        f"**Progress:** {progress_percentage * 100:.2f}%"
                    )

        status_placeholder.success(f"✅ Download completed: {file_path}")
        info_var.empty()
        progress_bar.empty()

    except RequestException as e:
        # Handle connection issues or invalid URL
        progress_bar.empty()
        status_placeholder.error(
            "❌ Failed to download the file. Please check your internet connection or if the URL is still valid."
        )
        st.error(f"Error details: {e}")
    except Exception as e:
        # Handle other unexpected issues
        progress_bar.empty()
        status_placeholder.error("❌ An unexpected error occurred during the download.")
        st.error(f"Error details: {e}")
