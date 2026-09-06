# Simple News Terminal TUI

A TUI news aggregator built with Textual.

## Usage

```bash
python main.py --config configs/configs.yaml
```

### Controls

| Key | Action |
|-----|--------|
| `t` | Toggle light/dark theme |
| `r` | Refresh current tab |
| `q` | Quit |
| `←/→` | Navigate tabs |

## Configuration

Edit `configs/configs.yaml`:

```yaml
news:
  urls:
    - https://vnexpress.net/
    - https://theinvestor.vn/
  block_list:
    - "#"
    - "comment"
number_of_news: 5
use_images: True
memoize_articles: False
theme: dark
page_size: 5
```