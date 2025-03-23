import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        """Test handling of empty Markdown input."""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_line(self):
        """Test Markdown with a single line."""
        md = "Just a **single** line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a **single** line"])

    def test_multiple_empty_lines(self):
        """Test Markdown with multiple consecutive empty lines."""
        md = """
First block

  
Second block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_only_whitespace(self):
        """Test Markdown with only whitespace."""
        md = "   \n\n  \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_nested_lists(self):
        """Test Markdown with nested list items."""
        md = """
- Top level
  - Nested item
  - Another nested
- Top level again
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["- Top level\n  - Nested item\n  - Another nested\n- Top level again"],
        )

    def test_code_block(self):
        """Test Markdown with a code block."""
        md = """
Paragraph before

```
This is a code block
Multiple lines
```

Paragraph after
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph before",
                "```\nThis is a code block\nMultiple lines\n```",
                "Paragraph after",
            ],
        )

    def test_markdown_to_block_types(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

1. first
2. second

# Heading

## Heading 2

### Heading 3

> Quote

>Quote2
"""
        block_types = list(
            map(lambda block: block_to_block_type(block), markdown_to_blocks(md))
        )
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.QUOTE,
                BlockType.QUOTE,
            ],
        )

    def test_code_block_to_block_types(self):
        """Test Markdown with a code block."""
        md = """
Paragraph before

```
This is a code block
Multiple lines
```

Paragraph after
"""
        block_types = list(
            map(lambda block: block_to_block_type(block), markdown_to_blocks(md))
        )
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.CODE,
                BlockType.PARAGRAPH,
            ],
        )


if __name__ == "__main__":
    _ = unittest.main()
