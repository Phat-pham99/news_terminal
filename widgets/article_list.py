from typing import List

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, ListItem, ListView, Static


class ArticleListItem(ListItem):
    def __init__(self, title: str, url: str, index: int):
        super().__init__(Static(f"{index + 1}. {title}"), id=f"article-{index}")
        self.title = title
        self.url = url
        self.index = index


class ArticleList(Static):
    def __init__(self, page_size: int = 5):
        super().__init__()
        self.page_size = page_size
        self.current_page = 0
        self.articles: List = []

    def compose(self) -> ComposeResult:
        yield ListView(id="article-list")
        yield Horizontal(
            Button("Prev", id="prev-page", disabled=True),
            Static("Page 1/1", id="page-indicator"),
            Button("Next", id="next-page", disabled=True),
            id="pagination-controls",
        )

    def update_articles(self, articles: List) -> None:
        self.articles = articles
        self.current_page = 0
        self._render_page()

    def _render_page(self) -> None:
        list_view = self.query_one("#article-list", ListView)
        list_view.clear()

        start = self.current_page * self.page_size
        end = start + self.page_size
        page_articles = self.articles[start:end]

        for i, article in enumerate(page_articles):
            list_view.append(
                ArticleListItem(article.title, article.url, start + i)
            )

        total_pages = max(1, (len(self.articles) + self.page_size - 1) // self.page_size)
        indicator = self.query_one("#page-indicator", Static)
        indicator.update(f"Page {self.current_page + 1}/{total_pages}")

        prev_btn = self.query_one("#prev-page", Button)
        next_btn = self.query_one("#next-page", Button)
        prev_btn.disabled = self.current_page == 0
        next_btn.disabled = self.current_page >= total_pages - 1

    def next_page(self) -> None:
        total_pages = (len(self.articles) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self._render_page()

    def prev_page(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1
            self._render_page()