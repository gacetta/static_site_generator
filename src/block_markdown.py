from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in new_blocks:
        cleaned = block.strip()
        if cleaned:
            cleaned_blocks.append(cleaned)
    # cleaned_blocks = [block.strip() for block in new_blocks if block.strip()]
    return cleaned_blocks

# def markdown_to_blocks(markdown):
#     blocks = markdown.split("\n\n")
#     filtered_blocks = []
#     for block in blocks:
#         if block == "":
#             continue
#         block = block.strip()
#         filtered_blocks.append(block)
#     return filtered_blocks

def block_to_block_type(markdown):
    def is_heading(block):
        if not block.startswith('#'):
            return False
        # Split into ['###', 'Heading text']
        parts = block.split(' ', 1)
        return len(parts) == 2 and 1 <= len(parts[0]) <= 6
    
    def is_code(block):
        if not block.startswith('```'):
            return False
        return block.endswith('```')
    
    def is_quote(block):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return False
        return True
    
    def is_unordered_list(block):
        lines = block.split("\n")
        for line in lines:
            if line.startswith("* ") or line.startswith("- "):
                continue
            return False
        return True
    
    def is_ordered_list(block):
        i = 1
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(f"{i}. "):
                return False
            i += 1
        return True
    
    if is_heading(markdown):
        return "heading"
    elif is_code(markdown):
        return "code"
    elif is_quote(markdown):
        return "quote"
    elif is_unordered_list(markdown):
        return "unordered_list"
    elif is_ordered_list(markdown):
        return "ordered_list"
    else:
        return "paragraph"