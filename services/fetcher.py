import re
from datetime import datetime
from typing import List

from newspaper import Source

from services.models import Article


def fetch_source(
    url: str,
    num_news: int,
    block_list: List[str],
    use_images: bool = False,
    memoize: bool = True,
) -> List[Article]:
    source = Source(url, memoize_articles=memoize)
    source.build()
    raw_articles = source.articles if source.articles else []

    filtered: List[Article] = []
    for article in raw_articles:
        if any(re.search(pattern, article.url) for pattern in block_list):
            continue
        if len(filtered) >= num_news:
            break

        try:
            article.download()
            article.parse()
        except Exception:
            continue

        date = _parse_date(article.publish_date)
        top_image = article.top_image if use_images else None

        filtered.append(
            Article(
                title=article.title,
                url=article.url,
                text=article.text,
                publish_date=date,
                top_image=top_image,
                source=url,
            )
        )

    return filtered


def _parse_date(raw) -> datetime:
    if raw is None:
        return datetime.min
    if isinstance(raw, datetime):
        return raw
    return datetime.min
