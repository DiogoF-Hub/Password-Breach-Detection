import gdown
import time

# Google Drive link
# The link should contain the shareable Google Drive URL
google_drive_file_id = "15YkzZwi1jeNE0cshQjPNcDPS8jmVatkO"
google_drive_url = f"https://drive.google.com/uc?id={google_drive_file_id}"


def download_file(output_file):
    print(f"Downloading {output_file} from Google Drive...")

    try:
        # Download the file
        gdown.download(google_drive_url, output_file, quiet=False)
        print(f"Download completed: {output_file}")
    except Exception:
        print(
            f"An error occurred during the download \n If error persists try to get it manually from https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader"
        )
        time.sleep(2)
