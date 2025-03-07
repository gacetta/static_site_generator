import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode

def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # only process TextNodes of TextType.TEXT
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        matching_images = extract_markdown_images(original_text)

        # if no images found, return node as is
        if not matching_images:
            new_nodes.append(old_node)
            continue
        
        for alt_text, url in matching_images:
            image_markdown = f"![{alt_text}]({url})"
            sections = original_text.split(image_markdown, 1)

            # raise Exception if the text isn't split properly into alt_text and url
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            # create a TextNode of text before image if it exists (not an empty string)
            leading_text = sections[0]
            if leading_text:
                new_nodes.append(TextNode(leading_text, TextType.TEXT))
                
            # create a TextNode of image
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # if there are more sections, move on to the next section
            if len(sections) > 1:
                original_text = sections[1]
        # create a TextNode of trailing text after image if it exists
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
         # only process TextNodes of TextType.TEXT
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        matching_links = extract_markdown_links(original_text)
        
        # if no links found, return node as is
        if not matching_links:
            new_nodes.append(old_node)
            continue

        for link_text, url in matching_links:
            link_markdown = f"[{link_text}]({url})"
            sections = original_text.split(link_markdown, 1)

            # raise Exception if the text isn't split properly into link_text and url
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            # create a TextNode of text before link if it exists (not an empty string)
            leading_text = sections[0]
            if leading_text:
                new_nodes.append(TextNode(leading_text, TextType.TEXT))

            # create a TextNode of link
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            # if there are more sections (possibly more text / link), iterate to next text
            if len(sections) > 1:
                original_text = sections[1]
        # create a TextNode of text after link if it exists (not an empty string)        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
        
    return new_nodes

def text_to_htmlnodes(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        if node.text_type == TextType.BOLD:
            html_nodes.append(HTMLNode("strong", node.text))
        elif node.text_type == TextType.ITALIC:
            html_nodes.append(HTMLNode("em", node.text))
        elif node.text_type == TextType.IMAGE:
            props = {
                "src": node.url,
                "alt": node.text
            }
            html_nodes.append(HTMLNode("img", "", None, props))
        elif node.text_type == TextType.LINK:
            props = {
                "href": node.url,
            }
            html_nodes.append(HTMLNode("a", node.text, None, props))
        else:
            html_nodes.append(HTMLNode(None, node.text))
    return html_nodes

def extract_markdown_images(text):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images = re.findall(image_regex, text)
    return images

def extract_markdown_links(text):
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links = re.findall(link_regex, text)
    return links

def extract_title(text):
    lines = text.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line.lstrip("# ").strip()
    raise ValueError("No h1 header found in text")