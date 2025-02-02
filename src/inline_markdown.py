from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        print(sections)
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

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.append(node)
        # else:
        #     text = node.text
        #     delimiter_offset = len(delimiter)
        #     # find positions of delimters
        #     start = text.find(delimiter)
        #     if start != -1:
        #         second_instance = text[start+delimiter_offset:].find(delimiter)

        #         if second_instance == -1:
        #             raise Exception("Invalid Markdown Syntax")
                
        #         end = second_instance + start + delimiter_offset
                
        #         text_1 = text[:start]
        #         text_2 = text[start+delimiter_offset:end]
        #         text_3 = text[end+delimiter_offset:]

        #         new_node_1 = TextNode(text_1, TextType.TEXT)
        #         new_node_2 = TextNode(text_2, text_type)
        #         new_node_3 = TextNode(text_3, TextType.TEXT)

        #         new_nodes.append(new_node_1)
        #         new_nodes.append(new_node_2)
        #         new_nodes.append(new_node_3)

        #     else:
        #         new_nodes.append(node)
    # return new_nodes