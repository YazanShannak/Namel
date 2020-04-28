import requests


class CrawlerBase:
    def __init__(self, url: str):
        self.url = url
        self.page_content = self.get_page(url)

    @staticmethod
    def get_page(url: str):
        return requests.get(url).content
