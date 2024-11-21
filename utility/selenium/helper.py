from pathlib import Path
from time import sleep
from lxml import html
import json


class ConvertWebElement:
    @staticmethod
    def toLxml(webElement: str):
        """Konversi Selenium WebElement menjadi lxml.HtmlElement"""
        if webElement is None:
            raise ValueError("webElement tidak boleh None")
        try:
            if webElement is None:
                raise ValueError("webElement tidak memiliki atribut 'innerHTML'")
            return html.fromstring(webElement)
        except Exception as e:
            raise RuntimeError(f"Error mengonversi WebElement ke lxml: {e}")


class Wait:
    WaitShort = 2
    WaitMedium = 4
    WaitLong = 6
    WaitVeryLong = 8

    @classmethod
    def waitShort(cls):
        sleep(cls.WaitShort)

    @classmethod
    def waitMedium(cls):
        sleep(cls.WaitMedium)

    @classmethod
    def waitLong(cls):
        sleep(cls.WaitLong)

    @classmethod
    def waitVeryLong(cls):
        sleep(cls.WaitVeryLong)


class ReadWriteJson:
    @staticmethod
    def writeToJson(data, file_path, mode="w"):
        with open(file_path, mode) as sp:
            json.dump(data, sp, indent=2, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def loadJson(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
