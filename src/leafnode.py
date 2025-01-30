from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value == None:
            raise ValueError("value is required and cannot be None")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag == None:
            return f"{self.value}"
        else:
            opening_tag = self.tag
            if self.props != None:
                opening_tag += self.props_to_html()
            opening_tag = f"<{opening_tag}>"
            closing_tag = f"</{self.tag}>"
            return opening_tag + self.value + closing_tag
