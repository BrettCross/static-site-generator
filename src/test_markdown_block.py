import unittest

from markdown_block import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownInline(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_empty(self):
        md = "This is **bolded** paragraph\n\n This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n\n\n- This is a list\n- with items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading_one(self):
        md = "# Heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    
    def test_block_to_block_type_heading_six(self):
        md = "###### Heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_block_to_block_type_heading_too_many(self):
        md = "####### Heading"
        block_type = block_to_block_type(md)
        self.assertNotEqual(
            block_type,
            BlockType.HEADING
        )

    def test_block_to_block_type_code(self):
        md = "```for(int i = 0; i < 3; i++)```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )
    
    def test_block_to_block_type_code_multi_line(self):
        md = "```for (int i = 0; i < 3; i++) {\nif (array[i] > max) {\nmax = array[i]\n}\n}```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )

    def test_block_to_block_type_quote_single(self):
        md = ">To be or not to be."
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )
    
    def test_block_to_block_type_quote_single_with_space(self):
        md = "> To be or not to be."
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )
    
    def test_block_to_block_type_quote_multi(self):
        md = "> To be or not to be.\n> To be or not to be.\n> To be or not to be."
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )

    def test_block_to_block_type_unordered_one(self):
        md = "- list item"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_unordered_multi1(self):
        md = "- list item\n- list item 2\n- list item 3"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_unordered_multi2(self):
        md = """- list item
- list item 2
- list item 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )
    
    def test_block_to_block_type_ordered_one(self):
        md = "1. list item"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_ordered_multi1(self):
        md = "1. list item\n2. list item\n3. list item"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_ordered_multi2(self):
        md = """1. list item
2. list item
3. list item"""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_paragraph1(self):
        md = "This is a paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_paragraph2(self):
        md = "This\nis\na\nparagraph"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_paragraph3(self):
        md = """This
is
a
paragraph"""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )