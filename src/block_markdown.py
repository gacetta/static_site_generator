from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes, text_to_htmlnodes

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_OLIST = "ordered_list"
BLOCK_TYPE_ULIST = "unordered_list"

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
        return BLOCK_TYPE_HEADING
    elif is_code(markdown):
        return BLOCK_TYPE_CODE
    elif is_quote(markdown):
        return BLOCK_TYPE_QUOTE
    elif is_unordered_list(markdown):
        return BLOCK_TYPE_ULIST
    elif is_ordered_list(markdown):
        return BLOCK_TYPE_OLIST
    else:
        return BLOCK_TYPE_PARAGRAPH
    
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
    new_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case "heading":
                new_nodes.append(block_header_to_htmlnode(block))
            case "code":
                new_nodes.append(block_code_to_htmlnode(block))
            case "quote":
                new_nodes.append(block_quote_to_htmlnode(block))
            case "unordered_list":
                new_nodes.append(block_list_to_htmlnode(block, "unordered"))
            case "ordered_list":
                new_nodes.append(block_list_to_htmlnode(block, "ordered"))
            case "paragraph":
                new_nodes.append(block_paragraph_to_htmlnode(block))
            case _:
                print(f"Unhandled block type: {block_type}")
                raise ValueError('Invalid Block Type')

    return ParentNode("div", new_nodes)

def block_header_to_htmlnode(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    return HTMLNode(f"h{count}", f"{block[count + 1:]}")

def block_code_to_htmlnode(block):
    code_text = ""
    lines = block[3:-3].split("\n")
    for line in lines:
        line = line.strip()
        code_text += line
    code_block = HTMLNode("code", code_text)
    return ParentNode("pre", [code_block])

def block_paragraph_to_htmlnode(block):
    child_html_nodes = text_to_htmlnodes(block)
    return ParentNode("p", child_html_nodes)

def block_quote_to_htmlnode(block):
    lines = block[1:].split(">")
    quote_text = ""
    for line in lines:
        quote_text += line + "\n"
    return HTMLNode("blockquote", quote_text)

def block_list_to_htmlnode(block, list_type="unordered"):
    list_tag = "ul"
    if list_type == "ordered":
        list_tag = "ol"
    lines = block.split("\n")
    children = []
    for line in lines:
        line = line.strip()
        children.append(HTMLNode("li", line))
    return ParentNode(list_tag, children)