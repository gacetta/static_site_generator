import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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
        
class TestParentNode(unittest.TestCase):
    def test_create_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children[0].tag, "b")
        self.assertEqual(node.children[0].value, "Bold text")
        self.assertEqual(len(node.children), 2)

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ]
        )

        # Produce result
        result = node.to_html()

        # Assertions for result
        expected_html = "<p><b>Bold text</b>Normal text</p>"
        self.assertEqual(result, expected_html)

    def test_create_nested_node(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [LeafNode(None, "Nested text")]
                ),
            ]
        )

        # Assertions for outer node
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 2)

        # Assertions for inner (nested) node
        nested_child = node.children[1]
        self.assertIsInstance(nested_child, ParentNode)
        self.assertEqual(nested_child.tag, "p")
        self.assertEqual(len(nested_child.children), 1)
        self.assertEqual(nested_child.children[0].value, "Nested text")

    def test_to_html_with_nested_node(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [LeafNode(None, "Nested text")]
                ),
            ]
        )

        # Produce Result
        result = node.to_html()
        # Assertions on Result
        expected_html = "<div><b>Bold text</b><p>Nested text</p></div>"
        self.assertEqual(result, expected_html)

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("a", []).to_html()

        self.assertEqual(str(context.exception), "Invalid HTML: no children provided")
    
    def test_create_ParentNode_with_props(self):
        props = {"class": "container", "id": "main"}
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Some text"),
            ],
            props=props
        )
        self.assertEqual(node.props, props)

    def test_to_html_with_props(self):
        props = {"class": "container", "id": "main"}
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Content"),
            ],
            props=props
        )
        result = node.to_html()
        expected_html = '<div class="container" id="main">Content</div>'
        self.assertEqual(result, expected_html)

    def test_to_html_without_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None,[LeafNode(None, "Content")]).to_html()

        self.assertEqual(str(context.exception), "Invalid HTML: no tag provided")

if __name__ == "__main__":
    unittest.main()