import os
from inline_markdown import extract_title
from block_markdown import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    # print a message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    # read the markdown file at from_path
    extracted_markdown = None
    with open(from_path, 'r') as from_file:
        extracted_markdown = from_file.read()

    # read the template file at template_path
    template_markdown = None
    with open(template_path, 'r') as template_file:
        template_markdown = template_file.read()

    # use markdown_to_html_node and .to_html() to convert markdown file to HTML string
    html_nodes = markdown_to_html_node(extracted_markdown)
    html_content = html_nodes.to_html()

    # use extract_title to grab title of page
    title = extract_title(extracted_markdown)

    # replace {{ Title }} and {{ Content }} placeholders in template with generated HTML and title
    final_html = template_markdown.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # write new full HTML page to file at dest_path
    # First ensure destination exists
    directory = os.path.dirname(dest_path)
    if directory:  # only try to create if there's actually a directory path
        os.makedirs(directory, exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # print a message
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}.")

    # Get a list of items from dir_path_content
    try:
        files = os.listdir(dir_path_content)
    except FileNotFoundError:
        print("Source directory does not exist")
        exit()

    # Iterate through files
    for file_name in files:
        # get file path name
        from_path = os.path.join(dir_path_content, file_name)
        dest_path = os.path.join(dest_dir_path, file_name)
        print(f" * {from_path} -> {dest_path}")

        # if the file is a file, generate a page:
        if os.path.isfile(from_path):
            # Check if the file is a Markdown file
            if file_name.endswith(".md"):
                # Replace the .md extension with .html for the destination path
                html_file_name = os.path.splitext(file_name)[0] + ".html"
                dest_path = os.path.join(dest_dir_path, html_file_name)
                print(f"Generating page from: {file_name} -> {html_file_name}")
                generate_page(from_path, template_path, dest_path)
            else:
                print(f"Skipping non-Markdown file: {file_name}")

        # if the file is a directory, ensure the directory exists in the destination
        if os.path.isdir(from_path):
            # Create the directory if it doesn't exist
            os.makedirs(dest_path, exist_ok=True)
            # Recursively process the directory
            generate_pages_recursive(from_path, template_path, dest_path)