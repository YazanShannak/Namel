from distributed_crawler.crawler.base import CrawlerBase
from lxml import html


class DataScraper(CrawlerBase):

    def __init__(self, url, required_data):
        super().__init__(url)
        self.required_data = required_data

    def parse_item(self):
        root = html.fromstring(self.page_content)
        sample = self.required_data.items()[0]
        data_value = root.xpath(sample[1])
        return {sample[0]: data_value}
