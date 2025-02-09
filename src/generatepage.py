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