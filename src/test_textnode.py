import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.yahoo.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.yahoo.com")
        self.assertEqual(node, node2)

    def test_eq_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is text node 1", TextType.BOLD)
        node2 = TextNode("This is text node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.yahoo.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.google.com")
        self.assertNotEqual(node, node2)


        


if __name__ == "__main__":
    unittest.main()