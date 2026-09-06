import re
from datetime import datetime
from typing import List

from newspaper import Article as NewspaperArticle
from newspaper import Source
from PIL import Image
import requests

from services.models import Article


def fetch_source(
    url: str,
    num_news: int,
    block_list: List[str],
    use_images: bool = False,
    memoize: bool = True,
) -> List[Article]:
    source = Source(url, memoize_articles=memoize)
    articles = source.articles if source.articles else []

    filtered: List[Article] = []
    for article in articles:
        if any(re.search(pattern, article.url) for pattern in block_list):
            continue

        try:
            newspaper_art = NewspaperArticle(url=article.url)
            newspaper_art.download()
            newspaper_art.parse()
        except Exception:
            continue

        date = _parse_date(article.publish_date)
        top_image = article.top_image if use_images else None

        filtered.append(
            Article(
                title=newspaper_art.title,
                url=article.url,
                text=newspaper_art.text,
                publish_date=date,
                top_image=top_image,
                source=url,
            )
        )

    return filtered[:num_news]


def _parse_date(raw) -> datetime:
    if raw is None:
        return datetime.min
    if isinstance(raw, datetime):
        return raw
    return datetime.min
