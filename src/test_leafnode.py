import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

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



if __name__ == "__main__":
    unittest.main()

