# News Terminal

A terminal-based news aggregator that fetches and displays articles from multiple sources directly in your terminal.

## Features

- **Multiple news sources** — Configure as many RSS/feed URLs as you want in `configs.yaml`
- **Tabbed interface** — Each news source gets its own tab; switch between them with arrow keys or mouse click
- **Article browser** — Browse paginated headlines in the left pane, read full articles in the right pane
- **Light / Dark mode** — Press `t` or use the header button to toggle themes
- **Image support** — Renders article images as unicode/ANSI art in the terminal
- **Keyboard-driven** — Fully navigable without touching the mouse

## Requirements

- Python 3.10+
- All dependencies in `requirements.txt`

## Installation

```bash
git clone https://github.com/Phat-pham99/news_terminal.git
cd news_terminal
python -m venv news_venv
source news_venv/bin/activate   # Linux/macOS
# news_venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Quick Start

```bash
python main.py
```

This reads `configs/configs.yaml` and launches the TUI.

## Usage

```
python main.py --config configs/configs.yaml
```

### Controls

| Key / Button | Action |
|---|---|
| `t` | Toggle between light and dark theme |
| `q` | Quit the application |
| `←` / `→` | Switch between news source tabs |
| Mouse click on tab | Switch to that news source |
| `Prev` / `Next` buttons | Navigate pages within the article list |

### Adding a custom news source at runtime

```bash
python main.py -u "https://example.com/feed"
```

## Configuration

Edit `configs/configs.yaml`:

```yaml
news:
  urls:
    - https://vnexpress.net/
    - https://theinvestor.vn/
    - https://dantri.com.vn/
  block_list:
    - "#"            # exclude URLs containing "#"
    - "comment"      # exclude URLs containing "comment"
    - "newsbtc.com/news/"
number_of_news: 5          # articles to fetch per source
use_images: True           # render article images as ASCII art
memoize_articles: False    # prevent duplicate articles across runs
theme: dark                # default theme: "dark" or "light"
page_size: 5              # articles shown per page in the list
```

## Project Structure

```
news_terminal/
├── main.py               # CLI entry point
├── app.py                # Textual TUI application
├── app.css               # Theme and layout styles
├── services/
│   ├── fetcher.py        # Newspaper-powered article fetching
│   └── models.py         # Article dataclass
├── widgets/
│   ├── header_bar.py     # Title bar + theme toggle button
│   ├── article_list.py   # Paginated article list
│   └── article_detail.py # Article text display pane
├── utils/
│   └── utils.py          # YAML config reader + image ASCII renderer
└── configs/
    ├── __init__.py
    └── configs.yaml
```

## How it works

`app.py` launches a Textual TUI. Each tab corresponds to one URL in `news.urls`. On tab activation, a background worker fetches articles via `services/fetcher.py` (which wraps `newspaper3k`), caches them, and renders a paginated list. Selecting an article displays its title, date, URL, and text in the detail pane.

## License

MIT