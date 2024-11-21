from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.utils import read_version_from_cmd
from webdriver_manager.core.os_manager import PATTERN
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def getDriver(headless: bool = False):
    # Membuat objek opsi untuk Firefox

    # if headless:
    #     options.add_argument("--headless")
    #     options.add_argument("--disable-gpu")
    #     options.add_argument("--window-size=1920x1080")
    # # options.add_argument("--disable-extensions")
    # # options.add_argument("--disable-infobars")
    # # options.add_argument("--disable-popup-blocking")
    # options.add_argument("--blink-settings=imagesEnabled=false")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--disable-notifications")

    # Menyusun driver dengan pengaturan Firefox dan path GeckoDriver yang tepat
    driver = webdriver.Chrome()

    return driver
