from mdtohtml import *
from textnode import *
from htmlnode import *
from helpers import *
import unittest

markdown ="""
# Heading 1 with *emphasis*

This is a basic paragraph.

## Heading 2 with **strong emphasis**

This is a paragraph with a [link](https://example.com) and *italic* text.

> This is a quote block with **bold** words.

- Item 1 with *italic*
- Item 2 with **strong**

1. First item with a [link](https://example.org)
2. Second item with `inline code`
"""

markdown2 = """
### heading *3*
"""

markdown3 = """
1. *one*
2. two
3. *three*
"""

markdown4 = "> this *isa*  quote"

markdown5 = """```this is a code block```"""


if __name__ == "__main__":
    unittest.main()