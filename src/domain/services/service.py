from abc import ABC, abstractmethod
from src.domain.models.article import Article
from ...infra.webscraper.kompasScraper import KompasScraper
from utility.chatGpt.chatGpt import run_ai
from utility.wordpress.helper import ToTemplateWP


class IArticleRepository(ABC):
    @abstractmethod
    def saveArticle(self, article: Article):
        pass

    @abstractmethod
    def articleExists(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def getArticleByUrl(self, url: str) -> Article:
        raise NotImplementedError


class Service:
    def __init__(
        self,
        driver,
        sourceUrl: dict,
        configScraping,
        wordpressApi,
        wordpress,
        repoArticle: IArticleRepository,
    ) -> None:
        super().__init__()
        self.kompas = KompasScraper(driver, sourceUrl, configScraping, wordpressApi)
        self.repo = repoArticle
        self.contentToTemplate = ToTemplateWP()
        self.wP = wordpress
        self.wPapi = wordpressApi

    def generateGpt(self):
        article = run_ai(generateContent="gpt")
        try:
            title = article[0]["content"]
            jsonFile = self.contentToTemplate.startCreateTemplate(article, title)
            if jsonFile is None:
                return

            importTemplateOk, templateId = self.wP.Template.import_template(
                str(jsonFile)
            )

            # jika error soon hapus images dan feaature image yg sudah di upload di server akan di download
            if importTemplateOk:
                print("TemplateID", templateId)
                _, response = self.wPapi.createPost(
                    title=title,
                    templateId=templateId,
                    excerpt="",
                    featuredMedia=67,
                )
                print(response)
        except:
            print("GPT not responding")
            return

    def scrapingHomePage(self):
        listOfArticles = self.kompas.scrapingHomePage()
        for articles in listOfArticles:
            for article in articles:
                print(article.category)
                print(article.url)

                # mengambil detail content artikel
                articleDetailContent = self.kompas.scrapingDetailArticle(article.url)

                # paraphrasing ke ai content yg sudah didapat
                articleParaphrasing = run_ai(articleDetailContent)
                jsonFile = self.contentToTemplate.startCreateTemplate(
                    articleParaphrasing,
                    article.title,
                )

                # upload ke wordpress
                if jsonFile is None:
                    return

                importTemplateOk, templateId = self.wP.Template.import_template(
                    str(jsonFile)
                )

                # jika error soon hapus images dan feaature image yg sudah di upload di server akan di download
                if importTemplateOk:
                    print("TemplateID", templateId)
                    _, response = self.wPapi.createPost(
                        title=article.title,
                        templateId=templateId,
                        excerpt=article.excerpt,
                        featuredMedia=article.featuredImage,
                    )
                    print("[**] Sukses create post", response)
