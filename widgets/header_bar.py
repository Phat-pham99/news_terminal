from textual.app import ComposeResult
from textual.widgets import Button, Header

from textual.binding import Binding


class NewsHeader(Header):

    BINDINGS = [
        Binding("t", "toggle_theme", "Toggle Theme", key_display="t"),
    ]

    def compose(self) -> ComposeResult:
        yield from super().compose()
        yield Button("Toggle Theme", id="toggle-theme", variant="primary")