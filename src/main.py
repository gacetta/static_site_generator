import os
import shutil
from copystatic import copy_files_recursive
from generatepage import generate_page, generate_pages_recursive

def main():
    # print(f"Current working directory: {os.getcwd()}")
    # print(f"Absolute static path: {os.path.abspath(static_path)}")
    # print(f"Absolute public path: {os.path.abspath(public_path)}")
    # print(f"copy_static from {static_path} to {public_path}")

    static_path = "static"
    public_path = "public"

    # Delete the "public" directory if it exists
    if os.path.exists(public_path):
        try:
            print(f"Deleting public directory...")
            shutil.rmtree(public_path)
        except PermissionError:
            print(f"Permission denied to copy to {public_path}")

    # Copy static files to the "public" directory
    print("Copying static files to public directory...")
    copy_files_recursive(static_path, public_path)

    # Generate all pages from the "content" directory recursively
    template_path = "template.html"
    content_path = "content"
    generate_pages_recursive(content_path, template_path, public_path)


if __name__ == "__main__":
    main()