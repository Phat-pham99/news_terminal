from datetime import datetime
from typing import Optional

from PIL import Image
import requests
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Static

from utils.utils import imagebit_to_string


class ArticleDetail(ScrollableContainer):
    def __init__(self, unicode: bool = True, image_width: int = 70):
        super().__init__()
        self.unicode = unicode
        self.image_width = image_width
        self.current_article: Optional[object] = None

    def compose(self) -> ComposeResult:
        yield Static("Select an article to view details", id="article-detail")

    def show_article(self, article) -> None:
        self.current_article = article
        detail = self.query_one("#article-detail", Static)

        date_str = ""
        if article.publish_date and article.publish_date != datetime.min:
            date_str = article.publish_date.strftime("%Y-%m-%d %H:%M")

        lines = [
            f"[bold cyan]{article.title}[/bold cyan]",
            f"[dim]{date_str}[/dim]" if date_str else "",
            f"[blue underline]{article.url}[/blue underline]",
            "",
        ]

        if article.top_image:
            try:
                img = Image.open(requests.get(article.top_image, stream=True).raw)
                img_str = imagebit_to_string(img, self.image_width, self.unicode)
                lines.append(img_str)
            except Exception:
                pass

        if article.text:
            lines.append("")
            lines.append(article.text[:1000])

        detail.update("\n".join(lines))