import os
import shutil

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from markdown_to_html import markdown_to_html_node


def copy_dir_to(src: str, dest: str):
    if not os.path.exists(src):
        raise ValueError(f"Can't copy from {src} because it doesn't exist")

    if os.path.isfile(src):
        raise ValueError(f"Can't copy from {src} because it is a file")

    if os.path.exists(dest):
        if os.path.isfile(dest):
            raise ValueError(f"Can't copy to {dest} because it is a file")
        shutil.rmtree(dest)

    os.mkdir(dest)

    for file in os.listdir(src):
        if os.path.isfile(os.path.join(src, file)):
            shutil.copy(os.path.join(src, file), os.path.join(dest, file))

        else:
            copy_dir_to(os.path.join(src, file), os.path.join(dest, file))


def extract_title(markdown: str) -> str:
    # This only works on the assumption that the title will be a direct child of the parent div
    # As there can be no other way to generate headings in our current logic
    blocks = markdown_to_blocks(markdown)
    block_types = list(map(lambda block: block_to_block_type(block), blocks))

    for block, block_type in zip(blocks, block_types):
        if block_type is not BlockType.HEADING:
            continue

        count = 0
        while block.startswith("#") and count < 6:
            block = block[1:]
            count += 1

        if block.startswith(" ") and count == 1:
            return block[1:]

    raise ValueError("No H1 Heading found, can't extract title")


def generate_pages(from_path: str, template_path: str, dest_path: str):
    if os.path.exists(os.path.join(from_path, "index.md")):
        generate_page(from_path, template_path, dest_path)

    for dir in os.listdir(from_path):
        if not os.path.isfile(os.path.join(from_path, dir)):
            generate_pages(
                os.path.join(from_path, dir),
                template_path,
                os.path.join(dest_path, dir),
            )


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(os.path.join(from_path, "index.md")) as markdown_file:
        markdown = markdown_file.read()
        html = markdown_to_html_node(markdown)
        title = extract_title(markdown)

    with open(template_path) as template_file:
        template = template_file.read()
        content = template.replace("{{ Title }}", title)
        content = content.replace("{{ Content }}", html.to_html())

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    write_content_to_file(os.path.join(dest_path, "index.html"), content)


def write_content_to_file(path: str, content: str):
    if os.path.exists(path) and not os.path.isfile(path):
        raise ValueError(f"Can't write content to {path} because it is a directory")

    with open(path, "a") as file:
        file.write(content)
