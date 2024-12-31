from textnode import *
from htmlnode import *
from helpers import *
from mdtohtml import *
from enum import Enum
import shutil
import os

def copy_files(source, destination):
    dirlist = os.listdir(source)
    for item in dirlist:
        if os.path.isfile(os.path.join(source, item)):
            shutil.copy(os.path.join(source, item), destination)
        else:
            os.mkdir(os.path.join(destination, item))
            copy_files(os.path.join(source, item), os.path.join(destination, item))

dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    shutil.rmtree("/home/raffkelly/workspace/github.com/raffkelly/static-site-generator/public/", True)
    os.mkdir("/home/raffkelly/workspace/github.com/raffkelly/static-site-generator/public/")
    copy_files("/home/raffkelly/workspace/github.com/raffkelly/static-site-generator/static/", "/home/raffkelly/workspace/github.com/raffkelly/static-site-generator/public/")

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()