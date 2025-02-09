class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None:
            return self.value
        children_html = ""
        if self.children:
            for child in self.children:
                children_html += child.to_html()
        if not self.value:
            self.value = ""
        return f"<{self.tag}{self.props_to_html()}>{self.value}{children_html}</{self.tag}>"
        
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