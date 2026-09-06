import asyncio
from typing import Dict, List

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, Header, ListView, Static, Tab, TabbedContent

from configs import load_config
from services.fetcher import fetch_source
from services.models import Article


class ArticleListView(Static):
    def __init__(self, page_size: int = 5, **kwargs):
        super().__init__(**kwargs)
        self.page_size = page_size
        self.current_page = 0
        self.articles: List[Article] = []

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ListView(id="article-list")
            with Vertical(id="pagination"):
                yield Button("Prev", id="prev-page", disabled=True)
                yield Static("Page 1/1", id="page-info")
                yield Button("Next", id="next-page", disabled=True)

    def update_articles(self, articles: List[Article]) -> None:
        self.articles = articles
        self.current_page = 0
        self._render_page()

    def _render_page(self) -> None:
        list_view = self.query_one("#article-list", ListView)
        list_view.clear()
        start = self.current_page * self.page_size
        end = start + self.page_size
        for i, article in enumerate(self.articles[start:end]):
            list_view.append(
                Static(f"[cyan]{start + i + 1}.[/cyan] [yellow]{article.title}[/yellow]")
            )
        total = max(1, (len(self.articles) + self.page_size - 1) // self.page_size)
        self.query_one("#page-info", Static).update(f"Page {self.current_page + 1}/{total}")
        self.query_one("#prev-page", Button).disabled = self.current_page == 0
        self.query_one("#next-page", Button).disabled = self.current_page >= total - 1

    def next_page(self) -> None:
        total = (len(self.articles) + self.page_size - 1) // self.page_size
        if self.current_page < total - 1:
            self.current_page += 1
            self._render_page()

    def prev_page(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1
            self._render_page()


class ArticleDetailView(Static):
    def compose(self) -> ComposeResult:
        yield Static("Select an article", id="detail-content")

    def show_article(self, article: Article) -> None:
        content = self.query_one("#detail-content", Static)
        date = article.publish_date.strftime("%Y-%m-%d") if article.publish_date else ""
        body = f"[bold cyan]{article.title}[/bold cyan]\n[dim]{date}[/dim]\n[blue]{article.url}[/blue]\n\n{article.text[:500]}"
        content.update(body)


class Vertical(Container):
    pass


class NewsApp(App):
    BINDINGS = [
        Binding("t", "toggle_theme", "Toggle Theme"),
        Binding("q", "quit", "Quit"),
    ]

    CSS_PATH = "app.css"

    def __init__(self, config_path: str = "configs/configs.yaml", **kwargs):
        super().__init__(**kwargs)
        self.config = load_config(config_path)
        self.current_theme = self.config.get("theme", "dark")
        self.page_size = self.config.get("page_size", 5)
        self.articles_cache: Dict[str, List[Article]] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        urls = self.config.get("news", {}).get("urls", [])
        tc = TabbedContent(id="source-tabs")
        for url in urls:
            host = url.split("://")[1].split("/")[0] if "://" in url else url
            tc.add_tab(
                Tab(
                    host,
                    Horizontal(
                        ArticleListView(page_size=self.page_size),
                        ArticleDetailView(),
                    ),
                )
            )
        yield tc
        yield Footer()

    def on_mount(self) -> None:
        self.apply_theme(self.current_theme)
        self.set_interval(0.5, self._check_tab_change)

    def _check_tab_change(self) -> None:
        pass

    def action_toggle_theme(self) -> None:
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(self.current_theme)


if __name__ == "__main__":
    app = NewsApp()
    app.run()