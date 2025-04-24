from markdown_block import markdown_to_html_node

def get_book_text(filepath):
    """takes a filepath as input and returns the contents of the file as a string."""
    
    with open(filepath) as f:
        file_contents = f.read()
    return file_contents


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # read markdown file at from_path, store in variable
    with open(from_path) as m:
        md = m.read()
        
    # read html file at template_path, store in variable
    with open(template_path) as h:
        template = h.read()
    # print(template)

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
    # print(template)

    # write new full page HTML to dest_path -> make sure to create all
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