import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("Hello `code` world", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "Hello ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " world")
    
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("Hello **bold** world", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "Hello ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " world")

    def test_split_nodes_delimiter_error_handling(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("Hello `code without closing tick", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(str(context.exception), "Invalid Markdown Syntax")
        
        # Should raise an exception


    # def test_connection(self):
    #     node = TextNode("This is text with a `code block` word", TextType.TEXT)
    #     new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    #     print(new_nodes)
    #     self.assertEqual(new_nodes, "test")