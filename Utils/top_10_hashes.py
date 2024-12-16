# heapq implements a heap-based priority queue. In this case, I'am using a min-heap to efficiently keep track of the top N hash counts while processing a large file line by line.
import heapq
import time
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
                file_size_bytes_saved = int(Ar[0])
                # line_count_saved = int(Ar[1])

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
                    line_count = count_lines(file_path)
                    write_cache(file_size_path, file_size_bytes, line_count)
                    return False
            else:  # If cache is empty, just write in file
                line_count = count_lines(file_path)
                write_cache(file_size_path, file_size_bytes, line_count)
                return False

    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def find_top_hashes(file_path, file_size_path, file_top10_path, top_n):
    print("\n")

    # If this returns True, it means the file size is the same as the one stored and there is already some top hashes stored so no need to compute them again
    # If not just compute again and save them into fileTop10.txt
    check_var = check_stored_file_size_and_top(
        file_path, file_size_path, file_top10_path, top_n
    )

    if check_var:
        counter = 0
        print(f"Top {top_n} hashes with the highest counts:")
        with open(file_top10_path, "r", encoding="utf-8") as file:
            for line in file:
                if counter == top_n:
                    break
                # end="" is so there is not a new line after each print and makes all prints together
                print(line, end="")
                counter += 1
    else:
        try:
            # Use a min-heap to track the top N hashes
            min_heap = []

            print(
                "Going through all the lines in the file. This might take a few seconds..."
            )

            # Open the file and process line by line
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    try:
                        # Split line into hash and count
                        hash_value, count = line.strip().split(":")
                        count = int(count)

                        # If the heap is not full, push the item.
                        # In this case the default is 10
                        if len(min_heap) < top_n:
                            heapq.heappush(min_heap, (count, hash_value))
                        else:
                            # Replace the smallest item if the current count is larger
                            # min_heap[0][0] is equal to the smallest count inside the heap
                            if count > min_heap[0][0]:
                                # This will push the next biggest found and it removes the smallest inside the heap
                                heapq.heappushpop(min_heap, (count, hash_value))
                    except ValueError:
                        print(f"Skipping malformed line: {line.strip()}")

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return

        # The top N hashes sorted by count in descending order
        top_hashes = sorted(min_heap, reverse=True)

        print("\n")

        print("Top 10 hashes with the highest counts:")

        # Save the results to a text file
        with open(file_top10_path, "w", encoding="utf-8") as out_file:
            # Enumerate will give a count to each hash and start by 1 and that will be in Rank variable
            for rank, (count, hash_value) in enumerate(top_hashes, start=1):
                # Writes the key and value from the array into a formated line which is count and hash_value
                line = f"{rank}. Count: {count}, Hash: {hash_value}\n"
                out_file.write(line)  # Write to file
                # end="" is so there is not a new line after each print and makes all prints together
                print(line, end="")  # Print to console

    time.sleep(4)
