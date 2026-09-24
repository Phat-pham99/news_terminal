from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    title: str
    url: str
    text: str = ""
    publish_date: Optional[datetime] = None
    top_image: Optional[str] = None
    source: str = ""
