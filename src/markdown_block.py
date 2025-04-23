from enum import Enum

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from markdown_inline import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block):
    """takes single markdown block as input and returns BlockType 
    representing the type of markdown block it is"""
    if is_block_heading(markdown_block):
        return BlockType.HEADING
    elif is_block_code(markdown_block):
        return BlockType.CODE
    elif is_block_quote(markdown_block):
        return BlockType.QUOTE
    elif is_block_unordered_list(markdown_block):
        return BlockType.UNORDERED_LIST
    elif is_block_ordered_list(markdown_block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    

def is_block_heading(text):
    if text.startswith("#") and text.strip("#")[0] == " ":
        splits = text.split()
        heading_num = len(splits[0])
        return 1 <= heading_num <= 6
    
    
def is_block_code(text):
    return text[:3] == "```" and text[-3:] == "```"


def is_block_quote(text):
    lines = text.split("\n")
    for line in lines:
        if line[0] != ">":
            return False
    return True


def is_block_unordered_list(text):
    lines = text.split("\n")
    for line in lines:
        if line[:2] != "- ":
            return False
    return True


def is_block_ordered_list(text):
    lines = text.split("\n")
    for i, line in enumerate(lines, 1):
        if line[:3] != f"{i}. ":
            return False
    return True


def markdown_to_blocks(markdown):
    """takes a raw markdown (representing a full document) string as input
    and returns a list of "block" strings.
    ex: The following would each be there own block 
    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item"""

    # blocks = [part.strip() for part in markdown.split("\n\n") if part != ""]
    new_blocks = []
    blocks = markdown.split("\n\n")

    for block in blocks:
        if block == "":
            blocks.remove(block)
            continue
    
        new_block = block.strip()
        
        new_blocks.append(new_block)


    return new_blocks


def markdown_to_html_node(markdown):
    """takes a full markdown document as input and
    returns a single parent HTMLNode. """
    children = []

    # split markdown into blocks
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        # determine type of block
        block_type = block_to_block_type(block)
        # create appropriate HTMLNode based on block & BlockType
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)

        # Assign the proper child HTMLNode objects to the block node. 
        # The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. 
    # Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
    parent = ParentNode(tag="div", children=children)
    return parent


def block_to_html_node(markdown, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_block_to_html_node(markdown)
        case BlockType.HEADING:
            return heading_block_to_html_node(markdown)
        case BlockType.CODE:
            return code_block_to_html_node(markdown)
        case BlockType.QUOTE:
            return quote_block_to_html_node(markdown)
        case BlockType.UNORDERED_LIST:
            return unordered_list_block_to_html_node(markdown)
        case BlockType.ORDERED_LIST:
            return ordered_list_block_to_html_node(markdown)
        case _:
            raise Exception(f"Unkown BlockType: {block_type}")
        

def text_to_html_node(markdown):
    """takes a markdown block as input and returns a list of LeafNodes"""
    children = []

    text_nodes = text_to_textnodes(markdown)
    
    for node in text_nodes:
        # print(f"node: {node}")
        child = text_node_to_html_node(node)

        children.append(child)
    return children


def paragraph_block_to_html_node(markdown):
    """takes a paragraph markdown block as input and returns a paragraph
        ParentNode with any children"""
    text = ""
    splitted = markdown.split("\n")

    for line in splitted:
        text += " " + line
    
    children = text_to_html_node(text.strip())
    parent = ParentNode(tag="p", children=children)
    return parent


def heading_block_to_html_node(markdown):
    """takes a heading markdown block and returns a heading ParentNode with any children"""
    splits = markdown.split()
    heading, heading_text = splits[0], " ".join(splits[1:])
    heading_num = len(heading)
    children = text_to_html_node(heading_text)
    parent = ParentNode(tag=f"h{heading_num}", children=children)
    # print(f"HTML: {parent.to_html()}")
    return parent


def code_block_to_html_node(markdown):
    """takes a code markdown block as input and returns a code ParentNode"""
    # inline code is single `
    # block code is triple ```
    text = markdown.strip("```")
    stripped_text = text.lstrip()

    child = text_node_to_html_node(TextNode(stripped_text, TextType.CODE, None))
    parent = ParentNode(tag="pre", children=[child])
    return parent


def quote_block_to_html_node(markdown):
    """takes a quote markdown block as input and returns a blockquote HTML ParentNode"""
    text = ""
    splits = markdown.split("\n")
    for line in splits:
        text += line.strip().strip(">")
    children = text_to_html_node(text.strip())
    return ParentNode(tag="blockquote", children=children)


def unordered_list_block_to_html_node(markdown):
    """
    - this is an item
    - another item
    - the last item
    """
    children = []
    splits = markdown.split("\n")
    for line in splits:
        text = text_to_html_node(line[2:])
        children.append(ParentNode(tag="li", children=text))

    parent = ParentNode(tag="ul", children=children)
    return parent 


def ordered_list_block_to_html_node(markdown):
    children = []
    splits = markdown.split("\n")
    for line in splits:
        text = text_to_html_node(line[3:])
        children.append(ParentNode(tag="li", children=text))

    # children = text_to_html_node(text.strip())
    parent = ParentNode(tag="ol", children=children)
    return parent