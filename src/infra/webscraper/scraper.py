from abc import ABC, abstractmethod


class Scraper(ABC):
    @abstractmethod
    def scrapingHomePage(self):
        pass

    @abstractmethod
    def scrapingDetailArticle(self):
        pass
