import unittest
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_create_node(self):
        node = LeafNode(
            "a", 
            "anchor node test", 
            {
                "href": "https://www.google.com",
            }
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "anchor node test")
        self.assertEqual(node.props, {
        "href": "https://www.google.com",
        })

    def test_create_node_with_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("a", None)

    def test_create_node_with_no_props(self):
        node = LeafNode(
            "a", 
            "anchor node test",
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.props, None)

    def test_create_node_with_children(self):
        node = LeafNode(
            "a", 
            "anchor node test", 
        )
        self.assertIsNone(node.children)

    def test_to_html(self):
        node = LeafNode(
            "a", 
            "anchor node test"
        )
        result = node.to_html()
        self.assertIn("<a>anchor node test</a>", result)

    def test_to_html_with_props(self):
        node = LeafNode(
            "a", 
            "anchor node test", 
            {
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        result = node.to_html()
        self.assertIn('<a href="https://www.google.com" target="_blank">anchor node test</a>', result)

    def test_to_html_with_no_tag(self):
        node = LeafNode(
            None, 
            "anchor node test"
        )
        result = node.to_html()
        self.assertIn("anchor node test", result)

    def test_to_html_with_no_value(self):
        node = LeafNode(
            "a", 
            "test"
        )
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()
        


if __name__ == "__main__":
    unittest.main()