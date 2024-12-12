import hashlib
from ...main import file_path


def add_hash_to_file(file_path):

    password = input("Enter the password you want to add: ")
    # while loop and try bcs the user might not type a number
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
    # hexdigest is for converting to hexadecimal string and upper to match the other hashes inside the file
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Format the line as "<hash>:<count>"
    entry = f"{sha1_hash}:{count}\n"

    # Append to the file (at the end)
    try:
        # "a" append in the file
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"Added hash: {sha1_hash} with count {count} to the end of {file_path}")
    except Exception as e:
        print(f"Error: {e}")


add_hash_to_file(file_path)
