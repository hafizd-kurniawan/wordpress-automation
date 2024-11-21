from dataclasses import dataclass
import tomllib


@dataclass
class ConfigData:
    databaseName: str
    KompasArticles: dict[str:str]
    KompasScraping: dict[str:str]
    WordpressData: dict[str:str]
    WordpressScraping: dict[str:str]


class Config:
    def __init__(self, configFile: str) -> None:
        self.configFile = configFile
        self.config = None

    def loadConfig(self) -> ConfigData:
        with open(self.configFile, "rb") as f:
            self.config = tomllib.load(f)
        return self.getData()

    def getData(self) -> ConfigData:
        dbName = self.config["database"]["name"]
        kompasArticle = self.config["kompasArticles"]
        kompasScraping = self.config["kompasScraping"]
        wordpressData = self.config["wordpress"]
        wordpressScraping = self.config["wordpressScraping"]
        return ConfigData(
            databaseName=dbName,
            KompasArticles=kompasArticle,
            KompasScraping=kompasScraping,
            WordpressData=wordpressData,
            WordpressScraping=wordpressScraping,
        )
