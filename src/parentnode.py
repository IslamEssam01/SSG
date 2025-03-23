from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")

        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have at least one child")

        return f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda x: x.to_html(),self.children))}</{self.tag}>"
