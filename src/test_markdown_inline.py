import unittest

from textnode import TextNode, TextType
from markdown_inline import split_nodes_delimiter

class TestMarkdownInline(unittest.TestCase):
    def test_split_nodes_delimiter_mid(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual (
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_multi(self):
        node = TextNode("This is text with one `code block` and another `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual (
            new_nodes,
            [
                TextNode("This is text with one ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and another ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ]
        )

    def test_split_nodes_delimiter_begin(self):
        node = TextNode("`code block` This started with one", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual (
            new_nodes,
            [
                TextNode("code block", TextType.CODE),
                TextNode(" This started with one", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_end(self):
        node = TextNode("This ends with one `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual (
            new_nodes,
            [
                TextNode("This ends with one ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ]
        )