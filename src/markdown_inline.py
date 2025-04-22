import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # if list is empty? 
    # no delimiter?
    # no text_type?
    # valid markdown? 
    new_nodes = []

    if old_nodes == []:
        raise Exception("Invalid input:old_nodes is empty")

    # TextNode("This is text with a `code block` word", TextType.TEXT)
    for old_node in old_nodes:
        if not old_node.text_type == TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_node = old_node.text.split(delimiter)
        # length is even, must be missing a delimiter
        if len(split_node) % 2 == 0:
            raise Exception(f"Invalid Markdown: missing a ' {delimiter} ' delimiter")
        
        # "This `code` that    => ["this", "code", "that"]
        # "`code block` this"  => ["", "code block", "this"]
        # "this `code block`"  => ["this", "code block", ""]
        for index, text in enumerate(split_node):
            if text == "":
                continue
            # must be TEXT type
            elif index % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        text = old_node.text

        images = extract_markdown_images(text)

        # no images are in old_node.text
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        # found images
        for i, image in enumerate(images, 1):

            # '' in split denotes where image is
            splits = text.split(f"![{image[0]}]({image[1]})", 1)

            img_node = TextNode(image[0], TextType.IMAGE, image[1])
            text_node = TextNode(splits[0], TextType.TEXT)

            # image is first
            if splits[0] == "":
                new_nodes.append(img_node)
            # image is last
            elif splits[1] == "":
                new_nodes.append(text_node)
                new_nodes.append(img_node)
            else:
                new_nodes.append(text_node)
                new_nodes.append(img_node)

            # last image or there's more to split
            if i == len(images) and splits[1] != "":
                text_node = TextNode(splits[1], TextType.TEXT)
                new_nodes.append(text_node)
            else:
                # split the text further through next iteration
                text = splits[1]

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        text = old_node.text

        links = extract_markdown_links(text)

        # no links in old_node.text
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        # found links
        for i, link in enumerate(links, 1):

            # '' in split denotes where link is
            splits = text.split(f"[{link[0]}]({link[1]})", 1)

            link_node = TextNode(link[0], TextType.LINK, link[1])
            text_node = TextNode(splits[0], TextType.TEXT)

            # link is first
            if splits[0] == "":
                new_nodes.append(link_node)
            # link is last
            elif splits[1] == "":
                new_nodes.append(text_node)
                new_nodes.append(link_node)
            else:
                new_nodes.append(text_node)
                new_nodes.append(link_node)

            # last link or there's more to split
            if i == len(links) and splits[1] != "":
                text_node = TextNode(splits[1], TextType.TEXT)
                new_nodes.append(text_node)
            else:
                # split the text further through next iteration
                text = splits[1]

    return new_nodes


def extract_markdown_images(text):
    """takes raw markdown text as input and returns a list of tuples,
    each tuple is the alt text and url of any markdown images"""
    # "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif 
    # returns - [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches


def extract_markdown_links(text):
    """takes raw markdown text as input and returns a list of tuples,
    each tuple is the anchor text and url of any markdown link"""
    regex = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches


def text_to_textnodes(text):
    """converts the input text to a list of TextNode objs and returns the list"""
    # start by creating a TextNode with a text that is the entire text input
    textnodes = split_nodes_delimiter([TextNode(text, TextType.TEXT, None)], "**", TextType.BOLD)
    
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)

    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)

    textnodes = split_nodes_image(textnodes)

    textnodes = split_nodes_link(textnodes)

    return textnodes