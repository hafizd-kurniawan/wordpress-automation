from src.domain.services.service import Service


class ScrapeAndPostArticleUseCase:
    def __init__(self, service: Service):
        self.services = service

    def execute(self, generateContent: str = "gpt", targetContent: int = 5):
        if generateContent == "gpt":
            for _ in range(10):
                self.services.generateGpt()
        else:
            article_data = self.services.scrapingHomePage()
            print(article_data)

        # # Create an Article object
        # article = Article(title=article_data["title"], content=article_data["content"])

        # # Save the article to the database
        # self.article_repository.save_article(article)

        # # Post the article to WordPress
        # post = self.post_repository.create_post(article_data)

        # return post
