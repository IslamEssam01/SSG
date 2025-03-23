from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType, textnode_to_htmlnode


def text_to_htmlnodes(text: str):
    return list(
        map(
            lambda textnode: textnode_to_htmlnode(textnode),
            text_to_textnodes(text),
        )
    )


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    block_types = list(map(lambda block: block_to_block_type(block), blocks))
    html_nodes: list[HTMLNode] = []

    for block, block_type in zip(blocks, block_types):
        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_htmlnodes(block.replace("\n", " "))
                html_nodes.append(ParentNode("p", children))
            case BlockType.HEADING:
                count = 0
                while block.startswith("#") and count < 6:
                    count += 1
                    block = block[1:]

                html_nodes.append(ParentNode(f"h{count}", text_to_htmlnodes(block[1:])))

            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_items: list[HTMLNode] = []

                for line in lines:
                    list_items.append(ParentNode("li", text_to_htmlnodes(line[2:])))

                html_nodes.append(ParentNode("ul", list_items))

            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_items: list[HTMLNode] = []

                for line in lines:
                    list_items.append(
                        ParentNode("li", text_to_htmlnodes(line[line.index(".") + 2 :]))
                    )

                html_nodes.append(ParentNode("ol", list_items))

            case BlockType.QUOTE:
                lines = block.split("\n")
                quote_items: list[HTMLNode] = []

                for line in lines:
                    quote_items.extend(
                        list(
                            map(
                                lambda textnode: textnode_to_htmlnode(textnode),
                                text_to_textnodes(line[1:]),
                            )
                        ),
                    )

                html_nodes.append(ParentNode("blockquote", quote_items))

            case BlockType.CODE:
                html_nodes.append(
                    ParentNode(
                        "pre",
                        [
                            ParentNode(
                                "code",
                                [
                                    textnode_to_htmlnode(
                                        TextNode(block[3:-3].lstrip(), TextType.TEXT)
                                    )
                                ],
                            )
                        ],
                    )
                )

    return ParentNode("div", html_nodes)


if __name__ == "__main__":
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    print(repr(markdown_to_html_node(md).to_html()))
