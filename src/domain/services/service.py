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

    def scrapingHomePage(self):

        # articleDetailContent = self.kompas.scrapingDetailArticle(
        #     "https://otomotif.kompas.com/read/2024/11/21/110200115/tanpa-bore-up-tingkatkan-performa-motor-dengan-modif-throttle-body#google_vignette"
        # )
        # print(articleDetailContent)
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
                templateId = self.wP.Template.import_template(str(jsonFile))
                print("TemplateID", templateId)
                _, response = self.wPapi.createPost(
                    title=article.title,
                    templateId=templateId,
                    excerpt=article.excerpt,
                    featuredMedia=article.featuredImage,
                )

                print("[**] Sukses create post", response)
