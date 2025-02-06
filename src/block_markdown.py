from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in new_blocks:
        cleaned = block.strip()
        if cleaned:
            cleaned_blocks.append(cleaned)
    return cleaned_blocks

def block_to_block_type(markdown):    
    if is_heading(markdown):
        return BlockType.HEADING
    elif is_code(markdown):
        return BlockType.CODE
    elif is_quote(markdown):
        return BlockType.QUOTE
    elif is_unordered_list(markdown):
        return BlockType.ULIST
    elif is_ordered_list(markdown):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH
    
def is_heading(block):
        block = block.strip()
        if not block.startswith('#'):
            return False
        parts = block.split(' ', 1)
        return len(parts) == 2 and 1 <= len(parts[0]) <= 6
    
def is_code(block):
    if not block.startswith('```'):
        return False
    return block.endswith('```')

def is_quote(block):
    lines = block.split("\n")
    for line in lines:
        line = line.strip()
        if not line.startswith(">"):
            return False
    return True

def is_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("* ") or line.startswith("- "):
            continue
        return False
    return True

def is_ordered_list(block):
    i = 1
    lines = block.split("\n")
    for line in lines:
        line = line.strip()
        if not line.startswith(f"{i}. "):
            return False
        i += 1
    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return header_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.ULIST:
            return list_to_html_node(block, "ul")
        case BlockType.OLIST:
            return list_to_html_node(block, "ol")
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case _:
            raise ValueError(f"Unhandled block type: {block_type}")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def header_to_html_node(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    if count + 1 >= len(block):
        raise ValueError(f"invalid heading level: {count}")
    text = block[count + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{count}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        line = line.strip()
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

# def olist_to_html_node(block):
#     items = block.split("\n")
#     html_items = []
#     for item in items:
#         item = item.strip()
#         dot_space_index = item.find(".")
#         if dot_space_index == -1:
#             raise ValueError("Invalid ordered list item")
#         text = item[dot_space_index + 2:]
#         children = text_to_children(text)
#         html_items.append(ParentNode("li", children))
#     return ParentNode("ol", html_items)

# def ulist_to_html_node(block):
#     print(f"Block received: '{block}'")
#     items = block.split("\n")
#     html_items = []
#     for item in items:
#         item = item.strip()
#         text = item[2:]
#         print(f"Text after removing marker: '{text}'") 
#         children = text_to_children(text)
#         html_items.append(ParentNode("li", children))
#     return ParentNode("ul", html_items)

def list_to_html_node(block, list_type="ul"):
    items = block.split("\n")
    html_items = []
    slice_value = 2
    for item in items:
        item = item.strip()
        if list_type == "ol":
            dot_space_index = item.find(".")
            if dot_space_index == -1:
                raise ValueError("Invalid ordered list item")
            slice_value = dot_space_index + 2
        text = item[slice_value:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode(list_type, html_items)