import re
from textnode import TextNode, TextType

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

def extract_markdown_images(text):
    # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    # print(extract_markdown_images(text))
    # # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images = re.findall(image_regex, text)
    return images

def extract_markdown_links(text):
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_links(text))
    # # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links = re.findall(link_regex, text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        # only process TextNodes of TextType.TEXT
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        matching_images = extract_markdown_images(original_text)

        if not matching_images:
            new_nodes.append(old_node)
            continue
        
        for alt_text, url in matching_images:
            image_markdown = f"![{alt_text}]({url})"
            sections = original_text.split(image_markdown, 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            leading_text = sections[0]

            if leading_text:
                new_nodes.append(TextNode(leading_text, TextType.TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            if len(sections) > 1:
                original_text = sections[1]
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
        if not matching_links:
            new_nodes.append(old_node)
            continue

        for alt_text, url in matching_links:
            link_markdown = f"[{alt_text}]({url})"
            sections = original_text.split(link_markdown, 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            leading_text = sections[0]

            if leading_text:
                new_nodes.append(TextNode(leading_text, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            if len(sections) > 1:
                original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
        
    return new_nodes

def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list