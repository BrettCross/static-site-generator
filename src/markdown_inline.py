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
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue    # ?
        

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