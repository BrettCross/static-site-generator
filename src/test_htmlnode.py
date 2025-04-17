import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html1(self):
        props1_dict = {"id":"header-title", "class":"title", "font-size":"24px"}
        node1 = HTMLNode("h1", "Heading Title", None, props1_dict)
        self.assertEqual (
            node1.props_to_html(),
            ' id="header-title" class="title" font-size="24px"'
        )
    
    def test_props_to_html2(self):
        child1 = HTMLNode("h1", "Heading Title", None, None)
        child2 = HTMLNode("p", "Description text here...", None, {"font-size": "10px"})
        props1_dict = {"id":"header-container", "class":"container", "margin":"auto"}
        node1 = HTMLNode("div", None, [child1, child2], props1_dict)
        self.assertEqual (
            node1.props_to_html(),
            ' id="header-container" class="container" margin="auto"'
        )

    def test_props_to_html3(self):
        node1 = HTMLNode("p", "Description text here...", None, None)
        self.assertEqual(node1.props_to_html(), "")

    def test_repr1(self):
        node1 = HTMLNode("h1", "Heading Title", None, None)
        str_repr = "HTMLNode(h1, Heading Title, None, None)"
        self.assertEqual(str_repr, repr(node1))
    
    def test_repr2(self):
        node1 = HTMLNode("h1", "Heading Title", None, {"id":"heading-title"})
        str_repr = "HTMLNode(h1, Heading Title, None, None)"
        self.assertNotEqual(str_repr, repr(node1))

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "This is paragraph text")
        self.assertEqual(node.to_html(), "This is paragraph text")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


class TestParentNode(unittest.TestCase):
    def test_parent_to_html1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_with_multi_children(self):
        child_node1 = LeafNode("p", "child")
        child_node2 = LeafNode("p", "child")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>child</p><p>child</p></div>",
        )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(
            parent_node.to_html(),
            "<div></div>",
        )

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), ' src="" alt=""')

    def test_link(self):
        node = TextNode("this is a link node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this is a link node")
        self.assertEqual(html_node.props_to_html(), ' href=""')

if __name__ == "__main__":
    unittest.main()