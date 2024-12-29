from textnode import *
from htmlnode import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            blocks = old_node.text.split(delimiter)
            if len(blocks) % 2 == 0: raise Exception("unmatched format character")
            for i in range(len(blocks)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(blocks[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(blocks[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        working_text = old_node.text
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            links = extract_markdown_links(old_node.text)
            if len(links) == 0:
                new_nodes.append(old_node)
                continue
            for i in range(len(links)):
                link_text = links[i][0]
                link_url = links[i][1]
                split_text = working_text.split(f"[{link_text}]({link_url})", 1)
                if split_text[0]: new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                if split_text[1] and i < (len(links)-1):
                    working_text = split_text[1]     
                elif split_text[1] and i == (len(links)-1):
                    new_nodes.append(TextNode(split_text[1], TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        working_text = old_node.text
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            images = extract_markdown_images(old_node.text)
            if len(images) == 0:
                new_nodes.append(old_node)
                continue
            for i in range(len(images)):
                image_text = images[i][0]
                image_url = images[i][1]
                split_text = working_text.split(f"![{image_text}]({image_url})", 1)
                if len(split_text) != 2:
                    raise ValueError("Invalid markdown, image section not closed")
                if split_text[0]: new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
                if split_text[1] and i < (len(images)-1):
                    working_text = split_text[1]     
                elif split_text[1] and i == (len(images)-1):
                    new_nodes.append(TextNode(split_text[1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    formatted_text = [TextNode(text, TextType.TEXT)]
    firststep = split_nodes_delimiter(formatted_text, "**", TextType.BOLD)
    secondstep = split_nodes_delimiter(firststep, "*", TextType.ITALIC)
    thirdstep = split_nodes_delimiter(secondstep, "`", TextType.CODE)
    fourthstep = split_nodes_link(thirdstep)
    final = split_nodes_image(fourthstep)
    return final

def markdown_to_blocks(markdown):
    split_doc = markdown.split("\n")
    blocked_doc = []
    block = ""
    for i in range(len(split_doc)):
        split_doc[i] = split_doc[i].strip(" ")
        if split_doc[i] == "":
            block = block.rstrip("\n")
            blocked_doc.append(block)
            block = ""
        elif split_doc[i] == split_doc[-1]:
            block += split_doc[i]
            blocked_doc.append(block)
        elif split_doc[i] != "":
            block += split_doc[i] + "\n"
    blocked_doc = list(filter(lambda x: x != "", blocked_doc))
    return blocked_doc


def block_to_block_type(block):
    if block[:3] == "```":
        block.replace("\n", " ")
    if block[:3] == "```" and block[-3:] == "```": return "code"
    
    if block[0] == "#":
        count = 1
        for i in range(1, 6):
            if block[i] == "#":
                count += 1
            else:
                break
        if count == 6 and block[6] == "#":
            return "paragraph"
        elif block[count] == " ":
            return "heading"
        else:
            return "paragraph"
        
    if block[0] == ">":
        block = block.strip()
        block_lines = block.split("\n")
        for line in block_lines:
            line = line.strip()
            if line[0] != ">":
                return "paragraph"
        return "quote"
        
    if (block[0] == "*" or block[0] == "-") and block[1] == " ":
        block = block.strip()
        block_lines = block.split("\n")
        for line in block_lines:
            line = line.strip()
            if ((line[0] != "*" and line[0] != "-") or line[1] != " "):
                return "paragraph"
        return "unordered_list"
    
    if block[0:3] == "1. ":
        block = block.strip()
        block_lines = block.split("\n")
        count = 0
        for line in block_lines:
            line = line.strip()
            count += 1
            if line[0:3] != f"{count}. ":
                return "paragraph"
        return "ordered_list"
    
    return "paragraph"