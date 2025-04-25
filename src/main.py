import os.path
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_page, generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
path_template = "./template.html"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)
    else:
        filepath = sys.argv[1]


def main():
    basepath = "/"

    if len(sys.argv) == 2:
        basepath = sys.argv[1]

    print(f"basepath: {basepath}")

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating html from md...")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(dir_path_content, path_template, dir_path_public, basepath)

main()