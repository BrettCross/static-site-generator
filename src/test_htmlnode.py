import unittest

from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()