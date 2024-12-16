import requests
import time

# Url to download the txt file with the hashes
# This url will work until the 12 of December of 2025
url = "https://365education-my.sharepoint.com/:u:/g/personal/cardi782_school_lu/ERKxnnAcYTZFuuhUJ9dflScBkutvLx5kOc0yLflGZe1O7w?e=rxlOXL&download=1"


def download_file(output_file):
    print(f"Downloading {output_file} from OneDrive...")
    time.sleep(2)  # wait 2s so the user can see the print above
    # stream=True is used to download the file in chunks and not all at the same time
    # So the RAM is not filled
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # wb - opens the file in binary write mode
    # The binary mode ensures that the file is written as raw bytes, which is important when saving non-text files or downloading large text files without any encoding issues
    with open(output_file, "wb") as file:
        # iter_content retrieve the response content in smaller chunks, instead of downloading the entire file at once
        # chunk_size defines the size which in this case is 5MB
        # So response.iter_content(chunk_size=...) iterates over the response data in 5MB chunks
        chunk_size = 5 * 1024 * 1024  # 5MB chunks
        downloaded = 0  # Define the downloaded size of file

        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
            downloaded += len(chunk)  # Update the downloaded size by adding the len

            # Display progress
            #: means that we are formating the output of that calculation
            # .2f will format the number as a floating-point value with 2 decimal places which will be in MB and not in bytes
            print(f"Downloaded: {downloaded / (1024 * 1024):.2f}MB")

    print(f"Download completed: {output_file}")
