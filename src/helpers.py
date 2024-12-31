from htmlnode import *
from textnode import *
import re
import os


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
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
                elif split_text[1] and i == (len(links)-1) and split_text[1] != "":
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
                elif split_text[1] and i == (len(images)-1) and split_text[1] != "":
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

def extract_title(markdown):
    markdown = markdown.rstrip()
    for line in markdown.splitlines():
        if line[0:2] == "# ":
            return line[2:]
    raise Exception("No title found in markdown document.")    