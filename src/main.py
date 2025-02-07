import os
import shutil
from copystatic import copy_files_recursive

def main():
    # print(f"Current working directory: {os.getcwd()}")
    # print(f"Absolute static path: {os.path.abspath(static_path)}")
    # print(f"Absolute public path: {os.path.abspath(public_path)}")
    # print(f"copy_static from {static_path} to {public_path}")

    static_path = "static"
    public_path = "public"

    if os.path.exists(public_path):
        try:
            print(f"Deleting public directory...")
            shutil.rmtree(public_path)
        except PermissionError:
            print(f"Permission denied to copy to {public_path}")

    print("Copying static files to public directory...")
    copy_files_recursive(static_path, public_path)

if __name__ == "__main__":
    main()