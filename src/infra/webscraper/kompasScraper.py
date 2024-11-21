from lxml import etree

from utility.selenium.seleniumDriver import SeleniumDriver
from config.config import ConfigData
from selenium import webdriver
from utility.utility.utility import Utils
from ..wordpress.wordpressApi import WordpressApi
from src.domain.models.article import Article
from utility.selenium.helper import ConvertWebElement
from utility.selenium.helper import Wait
from .scraper import Scraper


class KompasHomePageV1(SeleniumDriver):
    def __init__(
        self, driver: webdriver, configScraping: ConfigData, wordpressApi: WordpressApi
    ):
        super().__init__(driver)
        self.config = configScraping
        self.wpApi = wordpressApi
        self.foundImage = []

    def downloadImage(self, imgSrc: str, id=False) -> str:
        byteImage = Utils.downloadImageToBytes(imgSrc)
        response = self.wpApi.createMedia(
            contentType="image/*", filename="test.png", mediaBytes=byteImage
        )
        if id:
            return response[1]["id"]
        print("Success upload:", imgSrc)
        print(response[1]["url"])
        return response[1]["url"]

    ##############################
    # ekstrak artikel di dasboard halaman utama
    ##############################
    def extractUrl(self, element) -> list[str]:
        url = element.xpath(self.config["xpArticleLink"])
        return Utils.joinText(url)

    def extractTag(self, element):
        tag = element.xpath(self.config["xpArticleTag"])
        return Utils.joinText(tag)

    def extractTitle(self, element):
        title = element.xpath(self.config["xpArticleTitle"])
        title = Utils.joinText(title)
        return Utils.cleanText(title)

    def extractFeaturedImage(self, element) -> int:
        image = element.xpath(self.config["xpArticleFeaturedImage"])
        if isinstance(image, list):
            if len(image) == 0:
                return Utils.joinText(image)
            return self.downloadImage(image[len(image) - 1], id=True)
        return Utils.joinText(image)

    def extractExcerpt(self, element):
        text = element.xpath(self.config["xpArticleExcerpt"])
        if text is not None:
            return Utils.joinText(text)
        return None

    #########################
    # ekstrak detail artikel
    #########################
    def extractDetailArticleHeaderH1(self, element) -> dict[str:str]:
        h1Elements = element.xpath(self.config["xpDetailArticleTitle"])
        if h1Elements:
            return {"tag": "h1", "content": h1Elements[0]}

    def extractDetailArticleHeaderImage(self, element) -> dict[str:str]:
        imgElements = element.xpath(self.config["xpDetailArticleImage"])
        if imgElements:
            imgSrc = imgElements[0].get("src", "")
            imgAlt = imgElements[0].get("alt", "")
            return {"tag": "img", "src": self.downloadImage(imgSrc), "alt": imgAlt}

    def extractDetailArticleParagraph(self, tag, text) -> dict[str:str]:
        text = text.replace("KOMPAS.com", "PT. XYZ")
        if text:
            return {"tag": tag, "content": text}

    def extractDetailArticleImage(self, element) -> dict[str:str]:
        imgSrc = element.get("src", "")
        if imgSrc:
            return {"tag": "img", "src": imgSrc, "alt": element.get("alt", "")}

    def extractDetailArticleLi(self, tag, text) -> dict[str:str]:
        return {"tag": tag, "content": text}

    def extractDetailArticleDiv(self, element) -> dict[str:str]:
        el = element.xpath(self.config["xpPhotoWrap"])
        index = 0
        if len(el) != 0:
            # html_string = etree.tostring(el[0], pretty_print=True, encoding="unicode")
            imgElement = el[0].xpath(self.config["xpImageDescription"])
            if imgElement is not None:
                imgSrc = imgElement[index].get("src", "")
                if imgSrc in self.foundImage:
                    index = len(self.foundImage)
                    imgElementLength = len(imgElement)
                    if imgElementLength > index:
                        imgSrc = imgElement[index].get("src", "")

                self.foundImage.append(imgSrc)
                alt = imgElement[index].get("alt", "")
                return {
                    "tag": "img",
                    "src": self.downloadImage(imgSrc),
                    "alt": alt,
                }

    def extractDetailArticleHeading(self, tag, text) -> dict[str:str]:
        return {"tag": tag, "content": text}

    def extractDetailArticleContent(self, pageTree) -> list[str]:
        divArticles = pageTree.xpath(self.config["xpDetailArticles"])
        content = []
        foundImageContent = []

        # header H1 and header img
        content.append(self.extractDetailArticleHeaderH1(pageTree))
        content.append(self.extractDetailArticleHeaderImage(pageTree))

        if not divArticles:
            print("Div utama artikel tidak ditemukan.")

        # Mendapatkan konten artikel dengan
        # mengiterasi semua element
        for element in divArticles[0].iter():
            tag = element.tag

            # Mengabaikan elemen yang memiliki tag selain yg sudah ditenukan
            if tag not in self.config["targetTag"]:
                continue
            # Mengabaikan elemen yang memiliki atribut tertentu
            if any(attr in element.attrib for attr in self.config["xpIgnoreAttrib"]):
                continue

            text = element.text_content().strip()
            # if tag == "img":
            #     elImg = self.extractDetailArticleImage(element)
            #     imgSrc = elImg.get("src", "") if elImg is not None else None
            #     if elImg is not None and imgSrc not in foundImageContent:
            #         content.append(imgSrc)
            #         foundImageContent.append(imgSrc)
            #     continue

            if tag == "p":
                elP = self.extractDetailArticleParagraph(tag, text)
                if elP is not None:
                    content.append(elP)
                continue

            if tag == "div":
                elDiv = self.extractDetailArticleDiv(element)
                imgSrc = elDiv.get("src", "") if elDiv is not None else None
                if elDiv is not None and imgSrc not in foundImageContent:
                    content.append(elDiv)
                    foundImageContent.append(imgSrc)
                continue

            if tag in ["h2", "h3", "h4", "h5", "h6"]:
                elHeading = self.extractDetailArticleHeading(tag, text)
                if elHeading is not None:
                    content.append(elHeading)
                continue

            if tag == "li":
                elLi = self.extractDetailArticleLi(tag, text)
                if elLi is not None:
                    content.append(elLi)
                continue

        # hapus daftar image di artikel
        # self.foundImageDescription.clear()
        print("Scraping Done")
        print(self.foundImage)
        self.foundImage.clear()
        return content

    def scrapingHomePage(self, category: str, url: str) -> list[Article]:
        """
        method ini akan mengamabil semua sub artikel di halaman depan,
        kemudian akan mengambil url,title, dll
        """
        self.driver.get(url)

        articles = self.getElementList(self.config["xpArticlesV1"], "xpath")
        dataArticles = []

        print("---------------")
        print(category)
        for article in articles:
            innerHtml = article.get_attribute("innerHTML")
            articleElement = ConvertWebElement.toLxml(innerHtml)

            # Buat objek Article untuk menyimpan data
            articleData = Article(
                url=self.extractUrl(articleElement),
                category=category,
                tag=self.extractTag(articleElement),
                title=self.extractTitle(articleElement),
                featuredImage=self.extractFeaturedImage(articleElement),
                excerpt=self.extractExcerpt(articleElement),
                content=None,
            )
            dataArticles.append(articleData)
        return dataArticles


class KompasScraper(Scraper):
    def __init__(
        self,
        driver: webdriver,
        sourceUrl: dict,
        configScraping,
        wordpressApi: WordpressApi,
    ) -> None:
        super().__init__()
        self.homePagev1 = KompasHomePageV1(driver, configScraping, wordpressApi)
        self.sourceurl = sourceUrl
        self.driver = driver

    def scrapingHomePage(self) -> list[list[Article]]:
        articles = []
        for category, url in self.sourceurl.items():
            if category in ["otomotif", "teknologi", "traveling"]:
                article = self.homePagev1.scrapingHomePage(category, url)
                articles.append(article)
        return articles

    def scrapingDetailArticle(self, url: str):
        try:
            self.driver.get(url)
        except Exception as e:
            print("error trying")
            self.driver.get(url)
        Wait.waitMedium()
        pageTree = ConvertWebElement.toLxml(self.driver.page_source)
        return self.homePagev1.extractDetailArticleContent(pageTree)
