import unittest

from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title_single(self):
        markdown = "# Heading Title Here\n\n"
        md_title = extract_title(markdown)
        self.assertEqual(
            md_title,
            "Heading Title Here"
        )

    def test_extract_title_multi_head(self):
        # invalid markdown but still extracts Title
        markdown = "##### Header 5\n\n# Heading Title Here\n\n## Header 2\n\n### Header 3\n\n#### Header 4"
        md_title = extract_title(markdown)
        self.assertEqual(
            md_title,
            "Heading Title Here"
        )

    def test_extract_title_multi_line(self):
        markdown = "`Code`\n\n# Heading Title Here\n\n- list item\n- list item\n- list item"
        md_title = extract_title(markdown)
        self.assertEqual(
            md_title,
            "Heading Title Here"
        )