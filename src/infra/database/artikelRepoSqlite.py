from ...domain.repositories.iarticleRepository import IArticleRepository
from .model import Article
from .model import Category
from .model import Tag


class ArticleRepositorySQLite(IArticleRepository):
    def __init__(self, session):
        self.dbSession = session

    def saveArticle(self, article: Article):
        try:
            sqlAritcle = Article(
                title=article.title,
                url=article.url,
                category=article.category,
                tag=article.tag,
                template=article.template,
                internal_link=article.internal_link,
                scraping_date=article.scraping_date,
            )
            self.dbSession.add(sqlAritcle)
            self.dbSession.commit()
            print("Article saved successfully.")
        except Exception as e:
            self.dbSession.rollback()
            print(f"Error saving article: {e}")

    def articleExists(self, url: str) -> bool:
        return self.dbSession.query(Article).filter_by(url=url).first() is not None

    def getArticleByUrl(self, url: str) -> Article:
        return self.dbSession.query(Article).filter_by(url=url).first()

    def updateArticleByUrl(self, url: str, **kwargs):
        try:
            article = self.dbSession.query(Article).filter_by(url=url).first()

            if not article:
                print(f"Article with URL {url} not found.")
                return

            for key, value in kwargs.items():
                if hasattr(article, key):
                    setattr(article, key, value)
                else:
                    print(f"Invalid attribute: {key} (skipped)")

            self.dbSession.commit()
            print(f"Article with URL {url} updated successfully.")
        except Exception as e:
            self.dbSession.rollback()
            print(f"Error updating article: {e}")

    def saveArticleTag(self, name: str):
        try:
            sqlTag = Tag(name=name)
            self.dbSession.add(sqlTag)
            self.dbSession.commit()
            print("Tag saved successfully")
        except Exception as e:
            self.dbSession.rollback()
            print(f"Error saving article:{e}")

    def tagExists(self, name: str) -> bool:
        return self.dbSession.query(Tag).filter_by(name=name).first() is not None

    def getArticleTag(self, name: str) -> int:
        tag = self.dbSession.query(Tag).filter_by(name=name).first()
        return tag.id

    def getArticleCategory(self):
        pass

"""
    db = ArticleRepositorySQLite(dbSession)
    article1 = Article(
        title="First Article",
        url="http://example.com/first1",
        category="Tech",
        tag="Python",
        template="Template 1",
        internal_link=None,
    )

    article2 = Article(
        title="First Article",
        url="http://example.com/first2",
        category="Tech",
        tag="Python",
        template="Template 1",
        internal_link=article1.id,
    )

    article = db.getArticleByUrl(article1.url)
    print("idArticle", article.id)

    tagExists = db.tagExists(article1.tag)
    idTag = 0
    # jika tag masih belum terbuat maka buat taga
    if not tagExists:
        db.saveArticleTag(article1.tag)
    else:
        idTag = db.getArticleTag(article1.tag)
    print("idTag", idTag)

    article1 = Article(
        title="First Article",
        url="http://example.com/first1",
        category="Tech",
        tag="Python",
        template="Template 1",
        internal_link=article2.id,
    )
    db.updateArticleByUrl(
        url=article1.url,
        category="New Category",
        template="Updated Template",
    )

"""
