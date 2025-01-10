import subprocess
import re
import streamlit as st
import os


def download_file(output_file):
    st.write(f"Downloading {output_file} from Google Drive...")

    try:
        progress_bar = st.progress(0)
        status_placeholder = st.empty()

        # Run the gdown command using subprocess
        google_drive_file_id = "1GWTW7KI6ifbUbyvmUs19TgnEGOocaMhY"
        google_drive_url = f"https://drive.google.com/uc?id={google_drive_file_id}"

        # gdown command
        process = subprocess.Popen(
            ["gdown", google_drive_url, "-O", output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        # Parse the output line by line
        for line in process.stdout:
            status_placeholder.text(line.strip())

            # Match percentage from the line
            match = re.search(r"(\d+)%", line)
            if match:
                progress = int(match.group(1))
                progress_bar.progress(progress / 100)

        # Wait for the process to finish
        process.wait()

        if process.returncode == 0:
            progress_bar.progress(100)
            status_placeholder.success(f"Download completed: {output_file}")
            return True
        else:
            raise Exception("Download failed.")

    except Exception as e:
        # Check for cookies.txt issue
        cookies_path = os.path.expanduser("~/.cache/gdown/cookies.txt")
        error_message = f"An error occurred during the download: {e}\n\n"
        if os.path.exists(cookies_path):
            error_message += (
                f"This might be caused by the `cookies.txt` file located at:\n\n"
                f"`{cookies_path}`\n\n"
                f"Please delete the file manually and try again.\n\n"
            )
        error_message += (
            f"If the error persists, try downloading it manually from: "
            f"https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader"
        )
        st.error(error_message)
        return False
