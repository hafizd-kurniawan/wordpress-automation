from abc import ABC, abstractmethod
from ...domain.models.article import Article
from src.domain.services.service import IArticleRepository


class Repository(IArticleRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session
