from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        if check_quote_block(block):
            return BlockType.QUOTE

    if block.startswith("#"):
        if check_heading_block(block):
            return BlockType.HEADING

    if block.startswith("-"):
        if check_unordered_list_block(block):
            return BlockType.UNORDERED_LIST

    if block.startswith("1"):
        if check_ordered_list_block(block):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def check_heading_block(block: str) -> bool:
    count = 0
    while block.startswith("#") and count < 6:
        count += 1
        block = block[1:]

    return block.startswith(" ")


def check_unordered_list_block(block: str) -> bool:
    for line in block.split("\n"):
        if len(line) < 2:
            return False
        if line[0] != "-" or line[1] != " ":
            return False
    return True


def check_ordered_list_block(block: str) -> bool:
    accumulator = 1
    for line in block.split("\n"):
        if len(line) < 3:
            return False
        if line[0] != str(accumulator) or line[1] != "." or line[2] != " ":
            return False
        accumulator += 1
    return True


def check_quote_block(block: str) -> bool:
    for line in block.split("\n"):
        if not line.startswith(">"):
            return False
    return True


def markdown_to_blocks(markdown: str) -> list[str]:

    blocks = markdown.split("\n\n")

    mapped = map(lambda block: block.strip(), blocks)
    filtered = filter(lambda block: block != "", mapped)

    return list(filtered)
