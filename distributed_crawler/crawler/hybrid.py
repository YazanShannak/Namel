from typing import List, Dict

from redisbloom.client import Client

from .base import Base


class Hybrid(Base):
    def __init__(self, url: str, required_data: List[Dict], redis_client: Client):
        super(Hybrid, self).__init__(url=url, required_data=required_data)
        self.redis = redis_client
        self.add_url_to_filter()
        self.scraped_data = None

    def get_urls_in_page(self) -> List[str]:
        return self.parse_urls(url=self.url,
                               page_content=self.response_content) if self.response_code == 200 else None

    def add_url_to_filter(self):
        if self.response_code == 200:
            self.redis.bfAdd("urls", self.url)

    def filter_existing_urls(self, urls: List[str]) -> List[str]:
        return [url for url in urls if self.redis.bfExists("visited_urls", url) == 0]

    def crawl(self):
        all_urls = self.get_urls_in_page()
        filtered_urls = self.filter_existing_urls(urls=all_urls)
        self._scrape_data()
        return filtered_urls, self.scraped_data
