import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestSplitDelimiter(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("Hello `code` world", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" world", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_delim_bold(self):
        node = TextNode("Hello **bold** world", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" world", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )
    
    def test_delim_italic(self):
        node = TextNode("Hello *italic* world", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" world", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_delim_bold_and_italic(self):
        node = TextNode("*italic* and **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            new_nodes
        )

    def test_delim_error_handling(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("Hello `code without closing tick", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(str(context.exception), "Invalid markdown, formatted section not closed")

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertIn(("rick roll", "https://i.imgur.com/aKaOqIh.gif"), images)
        self.assertIn(("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"), images)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            images
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            links
        )