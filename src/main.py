from textnode import *
from htmlnode import *

def main():
    test = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(test)

main()
