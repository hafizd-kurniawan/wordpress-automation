from pathlib import Path
import json


class ToTemplateWP:
    def __init__(self) -> None:
        self.baseTemplate = None
        self.loadBaseTemplate()

    def loadBaseTemplate(self):
        fileBase = "/home/biru/Project/final-wp-automation/utility/wordpress/assets/templates/template_base.json"
        jsonData = ReadWriteJson.loadJson(fileBase)
        self.baseTemplate = jsonData

    def createTitleTemplate(self, title):
        self.baseTemplate["title"] = title

    def createHref(self, content, href="#"):
        return (
            {
                "id": "165e6919",
                "settings": {
                    "editor": f'<p><a title="" href={href}>Baca juga: {content}</a></p>',
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 18, "sizes": []},
                    "typography_line_height_mobile": {
                        "unit": "em",
                        "size": 1.9,
                        "sizes": [],
                    },
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "-6",
                        "left": "0",
                        "isLinked": False,
                    },
                    "_margin_mobile": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "-26",
                        "left": "0",
                        "isLinked": False,
                    },
                    "typography_font_size_mobile": {
                        "unit": "px",
                        "size": 14,
                        "sizes": [],
                    },
                },
                "elements": [],
                "isInner": False,
                "widgetType": "text-editor",
                "elType": "widget",
            },
        )

    def createHeadingH1(self, content):
        return {
            "id": "3a25b649",
            "settings": {
                "title": content,
                "_element_width": "initial",
                "_element_custom_width": {"unit": "%", "size": 97.763},
                "header_size": "h1",
                "typography_typography": "custom",
                "typography_font_size": {"unit": "px", "size": 40, "sizes": []},
                "typography_font_size_mobile": {"unit": "px", "size": 22, "sizes": []},
                "_margin": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "20",
                    "left": "0",
                    "isLinked": False,
                },
                "_margin_mobile": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "10",
                    "left": "0",
                    "isLinked": False,
                },
            },
            "elements": [],
            "isInner": False,
            "widgetType": "heading",
            "elType": "widget",
        }

    def creaateHeading(self, content):
        return {
            "id": "76e9bd0c",
            "settings": {
                "title": content,
                "typography_typography": "custom",
                "typography_font_size_mobile": {"unit": "px", "size": 20, "sizes": []},
                "_margin_mobile": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "-18",
                    "left": "0",
                    "isLinked": False,
                },
                "_padding_mobile": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "0",
                    "left": "0",
                    "isLinked": True,
                },
                "typography_font_size": {"unit": "px", "size": 30, "sizes": []},
            },
            "elements": [],
            "isInner": False,
            "widgetType": "heading",
            "elType": "widget",
        }

    def createImage(self, src, alt):
        return {
            "id": "aa64e8b",
            "settings": {
                "editor": f'<p><img class="size-medium" src="{src}" alt="{alt}" width="750" height="500"/></p>',
                "_margin": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "-20",
                    "left": "0",
                    "isLinked": False,
                },
                "_margin_mobile": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "-30",
                    "left": "0",
                    "isLinked": False,
                },
                "_padding_mobile": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "0",
                    "left": "0",
                    "isLinked": False,
                },
            },
            "elements": [],
            "isInner": False,
            "widgetType": "text-editor",
            "elType": "widget",
        }

    def createParagraf(self, content):
        return {
            "id": "45ded6d5",
            "settings": {
                "editor": f"<p>{content}</p>",
                "typography_typography": "custom",
                "typography_font_size": {"unit": "px", "size": 18, "sizes": []},
                "typography_line_height_mobile": {
                    "unit": "em",
                    "size": 1.9,
                    "sizes": [],
                },
                "_margin": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "-6",
                    "left": "0",
                    "isLinked": False,
                },
                "_margin_mobile": {
                    "unit": "px",
                    "top": "0",
                    "right": "0",
                    "bottom": "-26",
                    "left": "0",
                    "isLinked": False,
                },
                "typography_font_size_mobile": {"unit": "px", "size": 14, "sizes": []},
            },
            "elements": [],
            "isInner": False,
            "widgetType": "text-editor",
            "elType": "widget",
        }

    def createUl(self, content):
        return {
            "id": "28f6a8a5",
            "settings": {
                "editor": content,
                "typography_typography": "custom",
                "typography_font_size": {"unit": "px", "size": 18, "sizes": []},
                "typography_font_size_mobile": {"unit": "px", "size": 14, "sizes": []},
            },
            "elements": [],
            "isInner": False,
            "widgetType": "text-editor",
            "elType": "widget",
        }

    def createLi(self, content):
        start_ul = "<ul>"
        end_ul = "</ul>"
        start_li = "<li>"
        end_li = "</li>"
        template = []
        for index, c in enumerate(content):
            if index == 0:
                template.append(f"{start_ul} {start_li} {c} {end_li}")
                continue
            if index == (len(content) - 1):
                template.append(f"{start_li} {c} {end_li} {end_ul}")
                continue

        template.append(f"{start_li} {c} {end_li}")
        res = "".join(template)
        return self.createUl(res)

    def startCreateTemplate(self, jsonData, fileName):
        storeTemplates = []
        contentLi = []
        # datas = ReadWriteJson.loadJson(jsonData)

        title = fileName
        self.createTitleTemplate(title)
        for data in jsonData:
            try:
                tag = data["tag"]
                content = data.get("content", "")
                src = data.get("src", "")
                alt = data.get("alt", "")
            except:
                print("ERRROR")
                print(jsonData)
                print(type(jsonData))
                return None

            if tag == "h1":
                res = self.createHeadingH1(content)
                storeTemplates.append(res)
            if tag == "img" and src != None:
                res = self.createImage(src, alt)
                storeTemplates.append(res)
            if tag in ["h2", "h3", "h4", "h5", "h6"]:
                res = self.creaateHeading(content)
                storeTemplates.append(res)
            if tag == "p":
                res = self.createParagraf(content)
                storeTemplates.append(res)
            if tag == "li":
                contentLi.append(content)
            if tag == "a":
                res = self.createHref(content)
                storeTemplates.append(res)

        if len(contentLi) != 0:
            content = self.createLi(contentLi)
            storeTemplates.append(content)

        self.baseTemplate["content"][1]["elements"][0]["elements"].clear()
        self.baseTemplate["content"][1]["elements"][0]["elements"].extend(
            storeTemplates
        )

        path = Path.cwd()
        templateFile = path / f"{fileName}.json"
        ReadWriteJson.writeToJson(self.baseTemplate, templateFile)
        print(f"[*] Create Template Success: {templateFile}")
        return templateFile


class ReadWriteJson:
    @staticmethod
    def writeToJson(data, file_path, mode="w"):
        with open(file_path, mode) as sp:
            json.dump(data, sp, indent=2, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def loadJson(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
