import os

file_path = "pwnedpasswords.txt"
file_size_path = "fileSize.txt"


def count_lines(file_path):
    """Count the total number of lines in the file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            line_count = 0  # Initialize a counter
            for line in f:  # Iterate through each line in the file
                line_count += 1  # Increment the counter for each line
            return line_count
    except FileNotFoundError:
        # This except is not really needed bcs its already being check at the beginning of main.py but just in case
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error counting lines: {e}")


def write_cache(file_size_path, file_size_bytes, line_count):
    # Write the file size and line count to the cache.
    with open(file_size_path, "w", encoding="utf-8") as w:
        w.write(f"{file_size_bytes}:{line_count}\n")


def count_size_lines(file_path, file_size_path):
    try:
        # Get the file size in bytes
        file_size_bytes = os.path.getsize(file_path)

        # Read the cache file
        with open(file_size_path, "r", encoding="utf-8") as r:
            first_line = r.readline().strip()
            if first_line:  # Cache is not empty
                Ar = first_line.split(":")
                file_size_bytes_saved = int(Ar[0])
                line_count_saved = int(Ar[1])

                # Check if the cached size matches the current size
                if file_size_bytes == file_size_bytes_saved:
                    return line_count_saved

        # Cache is empty or invalid, recalculate line count
        print("Counting total lines in the file. This might take a few seconds...")
        line_count = count_lines(file_path)

        # Update the cache
        write_cache(file_size_path, file_size_bytes, line_count)

        return line_count

    except Exception as e:
        raise Exception(f"An error occurred: {e}")
