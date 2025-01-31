import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_create_node(self):
        node = HTMLNode(
            "a", 
            "anchor node test", 
            [], 
            {
                "href": "https://www.google.com",
            }
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "anchor node test")
        self.assertEqual(node.props, {
        "href": "https://www.google.com",
        })

    def test_node_with_children(self):
        child1 = HTMLNode("p", "First paragraph")
        child2 = HTMLNode("p", "Second paragraph")
        parent_node = HTMLNode(
            "div",
            children=[child1, child2]
        )
        # Assert that the parent has 2 children
        self.assertEqual(len(parent_node.children), 2)
        # Assert that the children are the correct nodes
        self.assertEqual(parent_node.children[0].value, "First paragraph")

    def test_repr(self):
        node = HTMLNode(
            "a", 
            "anchor node test", 
            [], 
            {
                "href": "https://www.google.com",
            }
        )
        result = repr(node)
        self.assertIn("a", result)
        self.assertIn("anchor node test", result)
        self.assertIn("href", result)

    def test_props_to_html(self):
        node = HTMLNode(
            "a", 
            "anchor node test", 
            [], 
            {
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
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