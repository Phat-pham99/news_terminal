import asyncio
from typing import Dict, List, Optional

from textual.app import App, ComposeResult
from textual.theme import Theme
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, ListView, Static, TabbedContent, TabPane

from configs import load_config
from services.fetcher import fetch_source
from services.models import Article


class ArticleListView(Container):
    def __init__(self, page_size: int = 5, **kwargs):
        super().__init__(**kwargs)
        self.page_size = page_size
        self.current_page = 0
        self.articles: List[Article] = []

    def compose(self) -> ComposeResult:
        with Vertical():
            yield ListView(id="article-list")
            with Horizontal(id="pagination"):
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


class ArticleDetailView(Container):
    def compose(self) -> ComposeResult:
        yield Static("Select an article", id="detail-content")

    def show_article(self, article: Article) -> None:
        content = self.query_one("#detail-content", Static)
        date = article.publish_date.strftime("%Y-%m-%d") if article.publish_date else ""
        body = f"[bold cyan]{article.title}[/bold cyan]\n[dim]{date}[/dim]\n[blue]{article.url}[/blue]\n\n{article.text[:500]}"
        content.update(body)


class NewsApp(App):
    BINDINGS = [
        Binding("t", "toggle_theme", "Toggle Theme"),
        Binding("q", "quit", "Quit"),
    ]

    CSS_PATH = "app.css"

    def __init__(self, config_path: str = "configs/configs.yaml", **kwargs):
        super().__init__(**kwargs)
        self.config = load_config(config_path)
        self._theme_name: str = self.config.get("theme", "dark")
        self.page_size = self.config.get("page_size", 5)
        self.urls: List[str] = self.config.get("news", {}).get("urls", [])
        self.block_list: List[str] = self.config.get("news", {}).get("block_list", [])
        self.num_news: int = self.config.get("number_of_news", 5)
        self.use_images: bool = self.config.get("use_images", False)
        self.memoize: bool = self.config.get("memoize_articles", True)
        self._fetched: Dict[str, bool] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        yield TabbedContent(id="source-tabs")
        yield Footer()

    def on_mount(self) -> None:
        dark = Theme(name="dark", primary="#6699ff", dark=True)
        light = Theme(name="light", primary="#0066cc", dark=False)
        self.register_theme(dark)
        self.register_theme(light)
        self.theme = self._theme_name
        tc = self.query_one("#source-tabs", TabbedContent)
        for i, url in enumerate(self.urls):
            host = url.split("://")[1].split("/")[0] if "://" in url else url
            tc.add_pane(
                TabPane(
                    host,
                    Horizontal(
                        ArticleListView(page_size=self.page_size),
                        ArticleDetailView(),
                    ),
                    name=url,
                    id=f"pane-{i}",
                )
            )
        self._fetch_active_tab()

    def _get_active_pane(self) -> Optional[TabPane]:
        tc = self.query_one("#source-tabs", TabbedContent)
        return tc.active_pane

    def _fetch_active_tab(self) -> None:
        pane = self._get_active_pane()
        if pane is None:
            return
        url = pane.name
        if url in self._fetched:
            return
        self._fetched[url] = True
        self.run_worker(self._fetch_url(url, pane), exclusive=True)

    async def _fetch_url(self, url: str, pane: TabPane) -> None:
        loop = asyncio.get_running_loop()
        articles = await loop.run_in_executor(
            None, fetch_source, url, self.num_news, self.block_list, self.use_images, self.memoize
        )
        list_view = pane.query_one(ArticleListView)
        list_view.update_articles(articles)

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        self._fetch_active_tab()

    def action_toggle_theme(self) -> None:
        self._theme_name = "light" if self._theme_name == "dark" else "dark"
        self.theme = self._theme_name


if __name__ == "__main__":
    app = NewsApp()
    app.run()
