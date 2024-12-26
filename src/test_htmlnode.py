import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
