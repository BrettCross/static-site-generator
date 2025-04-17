class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        children - A list of HTMLNode objects representing the children of this node
        props - A dictionary of key-value pairs representing the attributes of the HTML tag. 
        For example, a link (<a> tag) might have {"href": "https://www.google.com"}"""
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Child classes expected to override"""
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            string = ""
            for prop in self.props:
                string += f' {prop}="{self.props[prop]}"'
            return string
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif not self.tag:
            return self.value
        elif not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        if self.children is None:
            raise ValueError("Missing children")
        html_str = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html_str += child.to_html()
        html_str += f'</{self.tag}>'
        return html_str
