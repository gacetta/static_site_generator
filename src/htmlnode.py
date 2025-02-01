from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
        
    def props_to_html(self):
        if self.props is None:
            return ""
        result_string = ""
        for key, value in self.props.items():
            result_string += f' {key}="{value}"'
        return result_string
    
    def __repr__(self):
        return f"""HTMLNode(
        tag: {self.tag},
        value: {self.value},
        children: {self.children},
        props: {self.props}
    )"""

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value == None:
            raise ValueError("value is required and cannot be None")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value provided")
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid HTML: no tag provided")
        if not self.children:
            raise ValueError("Invalid HTML: no children provided")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


    # def to_html(self):
    #     if self.tag == None:
    #         raise ValueError("Invalid HTML: no tag provided")
    #     if self.children == None or len(self.children) == 0:
    #         raise ValueError("Invalid HTML: no children provided")
        
    #     # Handle Props
    #     if self.props:
    #         attributes = " ".join(f'{key}="{value}"' for key, value in self.props.items())
    #         opening_tag = f"<{self.tag} {attributes}>"
    #     else:
    #         opening_tag = f"<{self.tag}>"
        
    #     def recursive_to_html(children, result=""):
    #         # base case
    #         if not children:
    #             return result
            
    #         # recursive case
    #         current_child = children[0]
    #         result += current_child.to_html()
    #         return recursive_to_html(children[1:], result)

    #     children_html = recursive_to_html(self.children)
    #     return f"{opening_tag}{children_html}</{self.tag}>"

            
def text_node_to_html_node(text_node):
    # Destructure the object's attributes into local variables
    text_type = text_node.text_type
    text = text_node.text
    url = text_node.url

    match (text_type):
        case TextType.TEXT:
            return LeafNode(None, text)
        case TextType.BOLD:
            return LeafNode("b", text)
        case TextType.ITALIC:
            return LeafNode("i", text)
        case TextType.CODE:
            return LeafNode("code", text)
        case TextType.LINK:
            return LeafNode("a", text, {"href": url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": url, "alt": text})
        case _:
            raise ValueError("invalid text type")