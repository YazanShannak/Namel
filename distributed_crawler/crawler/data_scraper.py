from .entities import Url
from lxml import html
import requests


class DataScraper:
    def __init__(self, url: Url):
        self.url_object = url
        self.page_content, self.response_code = self.get_page(self.url_object.url)
        self.url_object.response = self.response_code
        self.root = html.fromstring(self.page_content) if self.response_code == 200 else None

    @staticmethod
    def get_page(url: str):
        response = requests.get(url)
        return response.content, response.status_code

    @property
    def required_data(self):
        return self.url_object.data

    def _scrape_data(self):
        output = []
        for data_item in self.required_data:
            xpath = data_item.get("xpath")
            result = self.root.xpath(xpath)
            if result:
                result = result[0] if len(result) == 1 else result
                data_item["value"] = result
                output.append(data_item)
        return output

    def scrape_page(self):
        if self.response_code == 200:
            scraped_data = self._scrape_data()
            self.url_object.data = scraped_data
        return self.url_object.object
