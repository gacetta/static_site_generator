import unittest
from block_markdown import markdown_to_blocks

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n        * This is a list item\n        * This is another list item"
            ],
            blocks
        )

    def test_markdown_to_blocks_excessive_whitespace(self):
        markdown = """\n\n\n\n     # whitespace header\n\n\n\n
        trailing whitespace                             \n\n

                                    * leading whitespace"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# whitespace header",
                "trailing whitespace",
                "* leading whitespace"
            ],
            blocks
        )

    def test_markdown_to_blocks_single_block(self):
        markdown = "* single block list 1\n* single block list 2"

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "* single block list 1\n* single block list 2",
            ],
            blocks
        )