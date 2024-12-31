from helpers import *
from htmlnode import *
from textnode import *
from pathlib import Path
import os

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def block_type_tag(block):
    block_type = block_to_block_type(block)
    if block_type == "quote": return ["blockquote"]
    if block_type == "code": return ["pre", "code"]
    if block_type == "paragraph": return["p"]
    if block_type == "unordered_list": return ["ul", "li"]
    if block_type == "ordered_list": return ["ol", "li"]
    if block_type == "heading":
        if block[:6] == "######": return ["h6"]
        if block[:5] == "#####": return ["h5"]
        if block[:4] == "####": return ["h4"]
        if block[:3] == "###": return ["h3"]
        if block[:2] == "##": return ["h2"]
        if block[:1] == "#": return ["h1"]

def convert_paragraph_block(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def convert_heading_block(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def convert_unordered_list(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        text = line[2:]
        line_children = text_to_children(text)
        children.append(ParentNode("li", line_children, None))
    return ParentNode("ul", children, None)

def convert_ordered_list(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        text = line[3:]
        line_children = text_to_children(text)
        children.append(ParentNode("li", line_children, None))
    return ParentNode("ol", children, None)

def convert_quote_block(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def convert_code_block(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def convert_any_block(block):
    if block_to_block_type(block) == "paragraph": return convert_paragraph_block(block)
    if block_to_block_type(block) == "heading": return convert_heading_block(block)
    if block_to_block_type(block) == "quote": return convert_quote_block(block)
    if block_to_block_type(block) == "code": return convert_code_block(block)
    if block_to_block_type(block) == "ordered_list": return convert_ordered_list(block)
    if block_to_block_type(block) == "unordered_list": return convert_unordered_list(block)

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in md_blocks:
        html_blocks.append(convert_any_block(block))
    return ParentNode("div", html_blocks, None)



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_text = f.read()
    with open(template_path) as f:
        template_text = f.read()
    html_string = markdown_to_html_node(markdown_text).to_html()
    title = extract_title(markdown_text)
    html_string = template_text.replace('{{ Title }}', title).replace('{{ Content }}', html_string)
    os.makedirs(os.path.dirname(dest_path), mode=0o777, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(html_string)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)




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