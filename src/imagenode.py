from htmlnode import HTMLNode


class ImageNode(HTMLNode):
    def __init__(
        self,
        props: dict[str, str | None] | None = None,
    ):
        super().__init__("img", None, None, props)

    def to_html(self):
        return f"<img{self.props_to_html()}>"
