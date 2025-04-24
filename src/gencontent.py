import os.path
from markdown_block import markdown_to_html_node


def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    # crawl every entry in content dir
    # for each .md file found -> gen new .html using template
        # dest_dir_path directory structure should be same content_dir_path
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(content_dir_path):
        content_path = os.path.join(content_dir_path, filename)
        target_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(content_path):
            # generate the page in target_path
            target_path = target_path[:-3] + ".html"
            generate_page(content_path, template_path, target_path)
        else:
            generate_pages_recursive(content_path, template_path, target_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # read markdown file at from_path, store in variable
    with open(from_path) as m:
        md = m.read()
        
    # read html file at template_path, store in variable
    with open(template_path) as h:
        template = h.read()

    # use markdown_to_html_node and .to_html()to convert .md file to HTML string
    html_node = markdown_to_html_node(md)
    content = html_node.to_html()

    # use extract_title() to grab title
    title = extract_title(md)

    # replace {{ title }} and {{ content }} placeholders in template
    template = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
    )

    # write new full page HTML to dest_path -> make sure to create all
    # Might have to change the following to create directories...
    f = open(dest_path, "w")
    f.write(template)
    f.close()


def extract_title(md):
    """takes markdown document, md, as input and returns the h1 (#) heading text"""
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no title found")