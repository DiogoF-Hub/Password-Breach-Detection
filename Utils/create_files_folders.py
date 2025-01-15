import os


def create_folder(folder_path):
    os.makedirs(folder_path)


def create_txt_files(file_size_path):
    # This creates the file and writes nothing
    with open(file_size_path, "w", encoding="utf-8") as f:
        pass
