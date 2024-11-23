from utility.selenium import SeleniumDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from lxml import html
import time

from utility.selenium.helper import ConvertWebElement


class Wordpress(SeleniumDriver):
    def __init__(
        self,
        driver: webdriver,
        configData: dict[str:str],
        scrapingPath: dict[str:str],
    ):
        super().__init__(driver)
        self.driver = driver
        self.configData = configData
        self.sP = scrapingPath
        self.Template = Template(driver)

    def enter_username(self, username):
        username_element = self.waitForElement(locator=self.sP["idLogin"])
        self.sendKeys(username, element=username_element)

    def enter_password(self, password):
        password_element = self.waitForElement(locator=self.sP["idPas"])
        self.sendKeys(password, element=password_element)

    def submit(self):
        submit_element = self.waitForElement(locator=self.sP["idSubmit"])
        self.elementClick(element=submit_element)

    def login(self):
        print(self.sP)
        self.driver.get(self.sP["loginUrl"])
        self.enter_username(self.configData["username"])
        self.enter_password(self.configData["password"])
        self.submit()


class Template(SeleniumDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    ######################################
    # Locator
    ######################################
    _url_wp_template = "http://ptkaryaagungland.com/wp-admin/edit.php?post_type=elementor_library&tabs_group=library"
    _id_btn_import_template = "elementor-import-template-trigger"
    _xp_insert_file = "//input[@type='file']"
    _xp_btn_confirm = "//button[@class='dialog-button dialog-ok dialog-confirm-ok']"
    _css_btn_import_now = "input[id='e-import-template-action']"

    def clik_import_template(self):
        self.elementClick(locator=self._id_btn_import_template, locatorType="id")

    def insert_file(self, data):
        locator = self._xp_insert_file
        insert_element = self.waitForElementPresence(locator, locatorType="xpath")
        insert_element.send_keys(data)
        time.sleep(1)

    def click_import_now(self):
        btn_element = self.waitForElement(self._css_btn_import_now, locatorType="css")
        self.elementClick(element=btn_element)
        time.sleep(1)

    def click_confirm(self):
        self.elementClick(locator=self._xp_btn_confirm, locatorType="xpath")
        print("sleep 10detik")
        time.sleep(10)

    def getElementorIdTemplate(self, templateName):
        template = templateName.split("/")[-1].split(".json")[0]
        time.sleep(5)

        pageTree = ConvertWebElement.toLxml(self.driver.page_source)
        # hasil yg di dapat adalah post-101
        # postId = f'//a[contains(text(),"{template}")]/ancestor::tr/@id'
        id = 0
        try:
            y = pageTree.xpath(f"//a[contains(text(),'{template}')]/ancestor::tr/@id")[
                0
            ]
            id = y.split("-")[1]
        except:
            return None, 0
        return True, id

    def import_template(self, data) -> tuple[None, int]:
        self.driver.get(self._url_wp_template)
        self.clik_import_template()
        self.insert_file(data)
        self.click_import_now()
        try:
            self.click_confirm()
        except:
            pass
        return self.getElementorIdTemplate(data)


# p = POST(DRIVER)
# p.add_post()
