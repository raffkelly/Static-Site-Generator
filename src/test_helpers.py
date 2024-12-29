import unittest
from helpers import *
from textnode import *

class TestOldNodesToTextNodes(unittest.TestCase):

    def test_code_old_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(new_nodes, expected_new_nodes, "old nodes not split properly")

    def test_bold_old_node(self):
        node = TextNode("This **is text with** multiple **bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_new_nodes = [
    TextNode("This ", TextType.TEXT),
    TextNode("is text with", TextType.BOLD),
    TextNode(" multiple ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" words", TextType.TEXT)
]
        self.assertEqual(new_nodes, expected_new_nodes, "old nodes not split properly")


    def test_bold_and_code_old_node(self):
        node = [TextNode("This is text with a `code block` word", TextType.TEXT), TextNode("This **is text with** multiple **bold** words", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(split_nodes_delimiter(node, "**", TextType.BOLD), "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
    TextNode("This ", TextType.TEXT),
    TextNode("is text with", TextType.BOLD),
    TextNode(" multiple ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" words", TextType.TEXT)
]
        self.assertEqual(new_nodes, expected_new_nodes, "old nodes not split properly")

    def test_invalid_markdown_identifiers(self):
        node = TextNode("This **is text with** multiple **bold words", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_bold_and_italic(self):
        node = [TextNode("This is **bold** and this is *italic* text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(split_nodes_delimiter(node, "**", TextType.BOLD), "*", TextType.ITALIC)
        expected_new_nodes = [
            TextNode("This is ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" and this is ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" text", TextType.TEXT),
]
        self.assertEqual(new_nodes, expected_new_nodes, "old nodes not split properly")


class ExtractImageAndLinks(unittest.TestCase):

    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected_result, "markdown image not extracted properly")
    
    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result =extract_markdown_links(text)
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected_result, "markdown link not extracted properly")

    def test_split_two_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        result =[ 
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" and ", TextType.TEXT),
             TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
             ),
         ]
        self.assertEqual(new_nodes, result, "Links not splitting out correctly")

    def test_split_two_images(self):
        node = TextNode("This is text with an image ![boot dev image](https://www.boot.dev/logo.jpg) and ![youtube image](https://www.youtube.com/logo.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        result =[ 
             TextNode("This is text with an image ", TextType.TEXT),
             TextNode("boot dev image", TextType.IMAGE, "https://www.boot.dev/logo.jpg"),
             TextNode(" and ", TextType.TEXT),
             TextNode("youtube image", TextType.IMAGE, "https://www.youtube.com/logo.jpeg"
             ),
         ]
        self.assertEqual(new_nodes, result, "Links not splitting out correctly")

    def test_split_image_at_start_and_end(self):
        node = TextNode("![first image](https://www.boot.dev/logo.jpg) This is text with an image ![youtube image](https://www.youtube.com/logo.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        result =[ 
             TextNode("first image", TextType.IMAGE, "https://www.boot.dev/logo.jpg"),
             TextNode(" This is text with an image ", TextType.TEXT),
             TextNode("youtube image", TextType.IMAGE, "https://www.youtube.com/logo.jpeg"
             ),
         ]
        self.assertEqual(new_nodes, result, "Links not splitting out correctly")

    def test_split_links_at_start_and_end(self):
        node = TextNode("[first link](https://www.boot.dev) This is text with two links [youtube link](https://www.youtube.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        result =[ 
             TextNode("first link", TextType.LINK, "https://www.boot.dev"),
             TextNode(" This is text with two links ", TextType.TEXT),
             TextNode("youtube link", TextType.LINK, "https://www.youtube.com"
             ),
         ]
        self.assertEqual(new_nodes, result, "Links not splitting out correctly")

    def test_split_two_middle(self):
        node = TextNode("Start ![img1](url1) middle ![img2](url2) end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        result =[
            TextNode("Start ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, result, "Links not splitting out correctly")

    def test_all_kinds_to_text_nodes(self):
        text = '![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_texts = (text_to_textnodes(text))
        expected = [
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        self.assertEqual(new_texts, expected)

    def test_markdown_to_blocks_three_blocks(self):
        markdown = """
        # This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocked = markdown_to_blocks(markdown)
        expected = ['# This is a heading',
                    'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                    '''* This is the first list item in a list block
* This is a list item
* This is another list item''']
        self.assertEqual(blocked, expected)



    def test_markdown_to_blocks_one_block(self):
        markdown = '# This is a heading'
        blocked = markdown_to_blocks(markdown)
        expected = ['# This is a heading']
        self.assertEqual(blocked, expected)

    def test_block_to_block_type_ordered_list(self):
        block = """1. one
        2. two
        3. two
        4. four"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "ordered_list")


if __name__ == "__main__":
    unittest.main()