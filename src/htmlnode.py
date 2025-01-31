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
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return f"{self.value}"
        # else:
        #     opening_tag = self.tag
        #     if self.props != None:
        #         opening_tag += self.props_to_html()
        #     opening_tag = f"<{opening_tag}>"
        #     closing_tag = f"</{self.tag}>"
        #     return opening_tag + self.value + closing_tag
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"