import re
from typing import Callable

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    nodes: list[TextNode] = []
    for node in old_nodes:
        if not node.text_type is TextType.TEXT:
            nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax, all opening delimiters({delimiter}) should have closing ones"
            )

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                nodes.append(TextNode(sections[i], text_type))

    return nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    nodes: list[TextNode] = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            nodes.append(node)
            continue

        text = node.text
        for i, (image_alt, image_url) in enumerate(images):
            before_image, after_image = text.split(f"![{image_alt}]({image_url})")
            if before_image != "":
                nodes.append(TextNode(before_image, TextType.TEXT))
            nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            text = after_image
        if text != "":
            nodes.append(TextNode(text, TextType.TEXT))

    return nodes


def split_nodes_link(old_nodes: list[TextNode]):
    nodes: list[TextNode] = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            nodes.append(node)
            continue

        text = node.text
        for i, (link_text, link_url) in enumerate(links):
            before_link, after_link = text.split(f"[{link_text}]({link_url})")
            if before_link != "":
                nodes.append(TextNode(before_link, TextType.TEXT))
            nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = after_link
        if text != "":
            nodes.append(TextNode(text, TextType.TEXT))

    return nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    splitters: list[Callable[[list[TextNode]], list[TextNode]]] = [
        split_nodes_image,
        split_nodes_link,
        lambda nodes: split_nodes_delimiter(nodes, "`", TextType.CODE),
        lambda nodes: split_nodes_delimiter(nodes, "**", TextType.BOLD),
        lambda nodes: split_nodes_delimiter(nodes, "_", TextType.ITALIC),
    ]

    nodes = [TextNode(text, TextType.TEXT)]
    for splitter in splitters:
        nodes = splitter(nodes)

    return nodes
