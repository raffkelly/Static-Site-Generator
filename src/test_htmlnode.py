import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_single(self):
        node = HTMLNode("div", "test", None, {"class": "container"})
        result = node.props_to_html()
        self.assertEqual(result, ' class="container"', "props string not correctly created")

    def test_props_to_html_multiple(self):
        node = HTMLNode("div", "test", None, {"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"', "props string not correctly created")

    def test_props_to_html_none(self):
        node = HTMLNode("div", "test", None, None)
        result = node.props_to_html()
        self.assertEqual(result, '', "props string not correctly created")

    def test_repr(self):
        node = HTMLNode("div", "test", None, {"class": "container"})
        result = str(node)
        self.assertEqual(result, "HTMLNode: Tag=div Value=test Number of Children=0 Props={'class': 'container'}", "repr not creating successfully")

    def test_repr_none(self):
        node = HTMLNode(None, None, None, None)
        result = str(node)
        self.assertEqual(result, "HTMLNode: Tag=None Value=None Number of Children=0 Props=None", "all none repr not creating successfully")

    def test_repr_children(self):
        child_node = HTMLNode("p", "child text", None, None)
        parent_node = HTMLNode("div", None, [child_node], None)
        result = str(parent_node)
        self.assertEqual(result, "HTMLNode: Tag=div Value=None Number of Children=1 Props=None", "repr with child not creating successfully")

    def test_to_html_with_tag_and_props(self):
        node = LeafNode("a", "test value", {"class": "container"})
        result = node.to_html()
        self.assertEqual(result, '<a class="container">test value</a>')
    
    def test_to_html_no_tag_or_props(self):
        node = LeafNode(None, "test value", None)
        result = node.to_html()
        self.assertEqual(result, 'test value')

    def test_to_html_with_tag_no_props(self):
        node = LeafNode("a", "test value", None)
        result = node.to_html()
        self.assertEqual(result, '<a>test value</a>')

    def test_to_html_with_tag_no_props(self):
        node = LeafNode("a", "test value", None)
        result = node.to_html()
        self.assertEqual(result, '<a>test value</a>')

    def test_to_html_no_value(self):
        node = LeafNode("a", None, {"class": "container"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_tag_and_multiple_props(self):
        node = LeafNode("a", "test value", {"class": "container", "secondclass": "secondcontainer"})
        result = node.to_html()
        self.assertEqual(result, '<a class="container" secondclass="secondcontainer">test value</a>')
    
    def test_boot_example(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        result = node.to_html()
        self.assertEqual(result, '<a href="https://www.google.com">Click me!</a>')


    def test_parentnode_to_html_with_four_children(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
        result = node.to_html()
        self.assertEqual(result, '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>', 'parent node to html with four children no good')


    def test_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is a paragraph with "),
                        LeafNode("strong", "strong"),
                        LeafNode(None, " emphasis.")
                    ]
                ),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "First item"),
                        LeafNode("li", "Second item"),
                        LeafNode("li", "Third item"),
                    ]
                ),
            ]
        )
        result = node.to_html()
        expected_result = (
            "<div>"
                "<p>This is a paragraph with <strong>strong</strong> emphasis.</p>"
                "<ul>"
                    "<li>First item</li>"
                    "<li>Second item</li>"
                    "<li>Third item</li>"
                "</ul>"
            "</div>"
        )
        self.assertEqual(result, expected_result, 'Failed for nested parent nodes')

    def test_parentnode_to_html_with_no_children(self):
            node = ParentNode(
            "p", None)
            with self.assertRaises(ValueError):
                node.to_html()

    def test_mixed_content_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Text outside of tags"),
                LeafNode("em", "Emphasized text"),
                LeafNode(None, "More plain text"),
            ]
        )
        result = node.to_html()
        expected_result = (
            "<div>"
                "Text outside of tags"
                "<em>Emphasized text</em>"
                "More plain text"
            "</div>"
        )
        self.assertEqual(result, expected_result, 'Failed for mixed content in children')

if __name__ == "__main__":
    unittest.main()
