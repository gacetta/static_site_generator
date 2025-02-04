import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

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

    def test_block_to_block_type_heading(self):
        block = block_to_block_type("### heading")
        self.assertEqual(block, "heading")

    def test_block_to_block_type_incorrect_heading(self):
        block = block_to_block_type("####### incorrect heading")
        self.assertEqual(block, "paragraph")

    def test_block_to_block_type_code(self):
        block = block_to_block_type("```code```")
        self.assertEqual(block, "code")

    def test_block_to_block_type_incorrect_code(self):
        block = block_to_block_type("```code``")
        self.assertEqual(block, "paragraph")

    def test_block_to_block_type_quote(self):
        block = block_to_block_type(">quote line 1\n>quote line 2\n>quote line 3")
        self.assertEqual(block, "quote")

    def test_block_to_block_type_incorrect_quote(self):
        block = block_to_block_type(">quote line 1\n>quote line 2\nquote line 3")
        self.assertEqual(block, "paragraph")

    def test_block_to_block_type_unordered_list(self):
        block = block_to_block_type("* ul line 1\n- ul line 2\n* ul line 3")
        self.assertEqual(block, "unordered_list")

    def test_block_to_block_type_incorrect_unordered_list(self):
        block = block_to_block_type("* ul line 1\n*ul line 2\n* ul line 3")
        self.assertEqual(block, "paragraph")

    def test_block_to_block_type_ordered_list(self):
        block = block_to_block_type("1. ol line 1\n2. ol line 2\n3. ol line 3")
        self.assertEqual(block, "ordered_list")

    def test_block_to_block_type_incorrect_ordered_list(self):
        block = block_to_block_type("1. ol line 1\n2. ol line 2\n4. ol line 3")
        self.assertEqual(block, "paragraph")

    def test_block_to_block_type_paragraph(self):
        block = block_to_block_type("plain ol' paragraph text")
        self.assertEqual(block, "paragraph")
