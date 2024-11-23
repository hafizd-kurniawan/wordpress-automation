from src.application.usecases.scrapeAndPostArticleUseCase import (
    ScrapeAndPostArticleUseCase,
)
from src.domain.services.service import Service
from src.infra.database.model import migrate
from config.config import Config
from utility.selenium.webdriver import getDriver
from src.infra.wordpress.wordpressApi import WordpressApi
from src.infra.database.artikelRepoSqlite import ArticleRepositorySQLite
from utility.chatGpt.chatGpt import open_chatgpt
from src.infra.wordpress.wordpressScraper import Wordpress
import time


def main():
    configFile = "./config/config.toml"
    config = Config(configFile).loadConfig()

    databaseUrl = f"sqlite:///{config.databaseName}"
    dbSession = migrate(databaseUrl)

    open_chatgpt()
    driver = getDriver()
    wp = Wordpress(
        driver,
        config.WordpressData,
        config.WordpressScraping,
    )
    wp.login()

    wpApi = WordpressApi(config.WordpressData)
    repo = ArticleRepositorySQLite(dbSession)
    sourceUrl = config.KompasArticles
    configScraping = config.KompasScraping

    service = Service(driver, sourceUrl, configScraping, wpApi, wp, repo)
    userCase = ScrapeAndPostArticleUseCase(service)
    userCase.execute()


if __name__ == "__main__":
    main()
