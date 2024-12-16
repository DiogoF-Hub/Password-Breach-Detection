import hashlib
import random


def add_hash_to_random_line(file_path):
    # Ask the user for a password
    password = input("Enter the password you want to add: ")

    # Ask the user for the number of times this password has been seen
    while True:
        try:
            count = int(
                input(
                    "Enter the number of times this password has been seen in breaches: "
                )
            )
            break
        except ValueError:
            print("Please enter a valid number.")

    # Hash the password using SHA-1
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Format the line as "<hash>:<count>"
    entry = f"{sha1_hash}:{count}\n"

    try:
        print("Attempting to insert the line randomly, this might take some seconds...")
        # Read all lines from the file
        # This makes python load the file into the ram
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Generate a random position to insert the new entry
        random_position = random.randint(0, len(lines))

        # Insert the new entry at the random position
        lines.insert(random_position, entry)

        # Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(
            f"Added hash: {sha1_hash} with count {count} at line {random_position + 1} in {file_path}"
        )
    except Exception as e:
        print(f"Error: {e}")
