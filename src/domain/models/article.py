from dataclasses import dataclass
from typing import Optional


@dataclass
class Article:
    url: str
    category: str
    tag: str
    title: str
    featuredImage: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
