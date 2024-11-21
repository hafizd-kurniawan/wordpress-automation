from ...domain.repositories.iarticleRepository import IArticleRepository
from ...domain.models.article import Article


class ArticleRepositorySQLite(IArticleRepository):
    def __init__(self, session):
        self.dbSession = session

    def saveArticle(self, article: Article):
        self.dbSession.add(article)
        self.dbSession.commit()

    def articleExists(self, url: str) -> bool:
        return self.dbSession.query(Article).filter_by(url=url).first() is not None

    def getArticleByUrl(self, url: str) -> Article:
        return self.dbSession.query(Article).filter_by(url=url).first()
