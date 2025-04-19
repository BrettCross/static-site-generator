from enum import Enum

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