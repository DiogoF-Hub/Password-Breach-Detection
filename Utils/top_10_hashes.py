# heapq implements a heap-based priority queue. In this case, I'am using a min-heap to efficiently keep track of the top N hash counts while processing a large file line by line.
import heapq
import os
import time
import streamlit as st
from Utils.filecount import write_cache, check_file_db, count_size_lines
from Utils.path_var import file_path, file_size_path, file_top10_path


def check_stored_file_size_and_top(top_n):
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
                    return False
            else:  # If cache is empty, just write in file
                return False

    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def find_top_hashes(top_n):
    info_var = st.info("Searching the database...")
    status_placeholder = st.empty()
    progress_bar = st.empty()
    progressNumber = st.empty()

    if check_file_db() == False:
        info_var.empty()
        progress_bar.empty()
        return

    # Validation for top_n before anything
    if not isinstance(top_n, int) or top_n < 1 or top_n > 100:
        st.error("Invalid input: Top N must be an integer between 1 and 100.")
        info_var.empty()
        progress_bar.empty()
        return

    # Check the stored file size and top hashes
    check_var = check_stored_file_size_and_top(top_n)

    top_hashes_formatted = []

    if check_var:
        # Read cached results if available
        with open(file_top10_path, "r", encoding="utf-8") as file:
            line_count_cache = 0
            for line in file:
                top_hashes_formatted.append(line)
                line_count_cache += 1
                if line_count_cache == top_n:
                    break
        info_var.empty()
        return top_hashes_formatted
    else:
        try:
            # Use a min-heap to track the top N hashes
            min_heap = []

            # First, count the total lines for accurate progress tracking
            total_lines = count_size_lines()

            progress_bar.progress(0)
            start_time = time.time()  # Start tracking time

            # Open the file and process line by line
            with open(file_path, "r", encoding="utf-8") as file:
                for current_line_number, line in enumerate(file, start=1):
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

                    # Update progress every 100,000 lines
                    if (
                        current_line_number % 100000 == 0
                        or current_line_number == total_lines
                    ):
                        progress = current_line_number / total_lines
                        elapsed_time = time.time() - start_time
                        estimated_total_time = (
                            elapsed_time / current_line_number
                        ) * total_lines
                        remaining_time = estimated_total_time - elapsed_time

                        status_placeholder.markdown(
                            f"**Elapsed Time:** {elapsed_time:.2f}s  \n"
                            f"**Estimated Remaining Time:** {remaining_time:.2f}s"
                        )
                        progress_bar.progress(progress)
                        progressNumber.markdown(f"**Progress:** {progress * 100:.2f}%")

        except Exception as e:
            info_var.empty()
            progress_bar.empty()
            st.error(f"An error occurred: {e}")
            return

        # Get the file size in bytes and save it in txt file
        file_size_bytes = os.path.getsize(file_path)
        write_cache(file_size_bytes, total_lines)

        # Sort and save results
        top_hashes = sorted(min_heap, reverse=True)
        with open(file_top10_path, "w", encoding="utf-8") as out_file:
            for rank, (count, hash_value) in enumerate(top_hashes, start=1):
                hash_line_formatted = f"{rank}. Count: {count} - Hash: {hash_value}"
                out_file.write(f"{hash_line_formatted}\n")
                top_hashes_formatted.append(hash_line_formatted)

        info_var.empty()
        status_placeholder.empty()
        progress_bar.empty()
        progressNumber.empty()
        st.success("Analysis completed.")

        return top_hashes_formatted
