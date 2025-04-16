from textnode import TextNode, TextType

def main():
    dummy = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    # TextNode(This is some anchor text, link, https://www.boot.dev)
    print(dummy)


main()