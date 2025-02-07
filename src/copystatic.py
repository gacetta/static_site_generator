import os
import shutil

def copy_files_recursive(source_path, dest_path):
    # First ensure destination exists - os.path.exists
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        print(f"Created directory: {dest_path}")
    else:
        print(f"Directory already exists: {dest_path}")

    # Get a list of items
    try:
        files = os.listdir(source_path)
    except FileNotFoundError:
        print("Source directory does not exist")
        exit()

    # Iterate through items
    for file_name in files:
        # get file path name
        from_path = os.path.join(source_path, file_name)
        dest_path = os.path.join(dest_path, file_name)
        print(f" * {from_path} -> {dest_path}")

        # if the file is a file, copy it
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
            print(f"Copied: {file_name}")

        # what if it is a directory?
        else:
            copy_files_recursive(from_path, dest_path)