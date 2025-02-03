def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in new_blocks:
        cleaned = block.strip()
        if cleaned:
            cleaned_blocks.append(cleaned)
    # cleaned_blocks = [block.strip() for block in new_blocks if block.strip()]
    return cleaned_blocks

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks