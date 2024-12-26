import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_two(self):
        node = TextNode("This is a text node", TextType.IMAGE, "www.google.com")
        node2 = TextNode("This is a text node", TextType.IMAGE, "www.google.com")
        self.assertEqual(node, node2)
    
    def test_ineq(self):
        node = TextNode("This is a test", TextType.NORMAL)
        node2 = TextNode("This is a test", TextType.LINK, "www.reddit.com")
        self.assertNotEqual(node, node2)

    def test_ineq_two(self):
        node = TextNode("This is a test", TextType.LINK)
        node2 = TextNode("This is a test", TextType.LINK, "www.reddit.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
