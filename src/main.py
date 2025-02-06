from textnode import TextNode, TextType
import os
import shutil

def main():
    print(f"Current working directory: {os.getcwd()}")
    static_path = "static"
    public_path = "public"
    print(f"Absolute static path: {os.path.abspath(static_path)}")
    print(f"Absolute public path: {os.path.abspath(public_path)}")
    print(f"copy_static from {static_path} to {public_path}")
    build_site(static_path, public_path)

def copy_static(source_path, dest_path):
    # First ensure destination exists - os.path.exists
    if not os.path.exists(dest_path):
        # if it doesn't exist, create it
        os.mkdir(dest_path)
        print(f"Created directory: {dest_path}")
    else:
        print(f"Directory already exists: {dest_path}")

    # Then get a list of items
    try:
        files = os.listdir(source_path)
    except FileNotFoundError:
        print("Source directory does not exist")
        exit()

    # Iterate through them
    for file_name in files:
        # get file path name
        file_path = os.path.join(source_path, file_name)


        # if the file is a file, copy it
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest_path)
            print(f"Copied: {file_name}")

        # what if it is a directory?
        else:
            try:
                new_dir = os.path.join(dest_path, file_name)
                old_dir = os.path.join(source_path, file_name)
                os.mkdir(new_dir)
                print(f"Created directory: {new_dir}")
                copy_static(old_dir, new_dir)
            except PermissionError:
                print(f"Permission denied: {new_dir}")

def build_site(source, dest):
    # check that dest exists
    if os.path.exists(dest):
        # if so clean destination
        try:
            shutil.rmtree(dest)
            os.mkdir(dest)
            # create fresh destination
            print(f"Directory {dest} cleaned.  All previous contents removed")
        except PermissionError:
            print(f"Permission denied to copy to {dest}")
    # start copy process
    copy_static(source, dest)

if __name__ == "__main__":
    main()