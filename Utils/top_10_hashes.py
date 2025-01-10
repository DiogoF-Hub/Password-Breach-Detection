# heapq implements a heap-based priority queue. In this case, I'am using a min-heap to efficiently keep track of the top N hash counts while processing a large file line by line.
import heapq
import os
from Utils.filecount import count_lines, write_cache


def check_stored_file_size_and_top(file_path, file_size_path, file_top10_path, top_n):
    try:
        # Get the file size in bytes
        file_size_bytes = os.path.getsize(file_path)

        # Read the cache file
        with open(file_size_path, "r", encoding="utf-8") as r:
            first_line = r.readline().strip()
            if first_line:  # Cache is not empty
                Ar = first_line.split(":")
                # Array of 0 bcs the first element is the size in bytes
                file_size_bytes_saved = int(Ar[0])

                # Check if the cached size matches the current size
                if file_size_bytes == file_size_bytes_saved:
                    with open(file_top10_path, "r", encoding="utf-8") as q:
                        total_lines = 0  # Initialize a counter
                        for line in q:  # Loop through each line in the file
                            total_lines += 1  # Increment the counter by 1 for each line

                        if total_lines >= top_n:
                            return True
                        else:
                            return False
                else:
                    # line_count = count_lines(file_path)
                    # write_cache(file_size_path, file_size_bytes, line_count)
                    return False
            else:  # If cache is empty, just write in file
                # line_count = count_lines(file_path)
                # write_cache(file_size_path, file_size_bytes, line_count)
                return False

    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def find_top_hashes(file_path, file_size_path, file_top10_path, top_n):

    # Validation for top_n before anything
    if not isinstance(top_n, int) or top_n < 1 or top_n > 100:
        return

    # Check the stored file size and top hashes
    check_var = check_stored_file_size_and_top(
        file_path, file_size_path, file_top10_path, top_n
    )

    top_hashes_formatted = []

    if check_var:
        # Read cached results if available
        with open(file_top10_path, "r", encoding="utf-8") as file:
            line_count_cache = 0
            for line in file:
                top_hashes_formatted.append(line)
                line_count_cache = line_count_cache + 1
                if line_count_cache == top_n:
                    break
        return top_hashes_formatted
    else:
        try:
            # Use a min-heap to track the top N hashes
            min_heap = []

            # Open the file and process line by line and save the line count
            line_count = 0
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line_count = line_count + 1
                    try:
                        # Split line into hash and count
                        hash_value, count = line.strip().split(":")
                        count = int(count)

                        if len(min_heap) < top_n:
                            heapq.heappush(min_heap, (count, hash_value))
                        else:
                            if count > min_heap[0][0]:
                                heapq.heappushpop(min_heap, (count, hash_value))
                    except ValueError:
                        continue

        except FileNotFoundError:
            raise Exception(f"Error: File '{file_path}' not found.")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

        # Get the file size in bytes and save it in txt file
        file_size_bytes = os.path.getsize(file_path)
        write_cache(file_size_path, file_size_bytes, line_count)

        # Sort and save results
        top_hashes = sorted(min_heap, reverse=True)
        with open(file_top10_path, "w", encoding="utf-8") as out_file:
            for rank, (count, hash_value) in enumerate(top_hashes, start=1):
                hash_line_formatted = f"{rank}. Count: {count} - Hash: {hash_value}"
                out_file.write(f"{hash_line_formatted}\n")
                top_hashes_formatted.append(hash_line_formatted)

        return top_hashes_formatted
