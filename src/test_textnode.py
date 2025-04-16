import unittest

from textnode import TextNode, TextType

# test creates two TextNode objects with the same properties
# asserts that they are equal

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_false(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node1, node2)

    def test_eq_false2(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node!", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_eq_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node1, node2)

    def test_repr(self):
        node =  TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        str_repr = "TextNode(This is a text node, bold, https://www.boot.dev)"
        self.assertEqual(str_repr, repr(node))

    def test_repr2(self):
        node =  TextNode("", TextType.BOLD, "https://www.boot.dev")
        str_repr = "TextNode(, bold, https://www.boot.dev)"
        self.assertEqual(str_repr, repr(node))

    def test_repr3(self):
        node =  TextNode("This is a text node", TextType.BOLD)
        str_repr = "TextNode(This is a text node, bold, None)"
        self.assertEqual(str_repr, repr(node))

if __name__ == "__main__":
    unittest.main()