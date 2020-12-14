from typing import List, Dict

from redisbloom.client import Client

from .base import Base


class Hybrid(Base):
    def __init__(self, url: str, required_data: List[Dict], redis_client: Client):
        super(Hybrid, self).__init__(url=url, required_data=required_data)
        self.redis = redis_client
        self.add_url_to_filter(url=url)

    def add_url_to_filter(self, url: str):
        """
        A method that adds the current URL to the hashing table in Redis as a crawled URL
        :return: None
        """
        if self.response_code == 200:
            self.redis.bfAdd("visited_urls", url)

    def filter_existing_urls(self, urls: List[str]) -> List[str]:
        """
        A method that takes a list of urls, checks each one if already crawled by querying Redis Bloom Filter and,
        returns all URLs that haven't been crawled
        :param urls: All urls found in the page
        :type urls: List of string urls
        :return: Urls that aren't crawled by other nodes
        :rtype: List of filtered string urls
        """
        
        return [url for url in urls if self.redis.bfExists("visited_urls", url) == 0]

    def crawl(self):
        """

        :return: Tuple of filtered Urls and scraped data if exists
        :rtype: Tuple of two items, first is a list of strings the other is a list of dictionaries
        """
        if self.response_code == 200:
            all_urls = self.parse_urls(url=self.url,
                                       page_content=self.response_content) if self.response_code == 200 else None
            filtered_urls = self.filter_existing_urls(urls=all_urls)
            scraped_data = self._scrape_data()
            scraped_data = self.create_output(url=self.url, response=self.response_code,
                                              required_data=self.required_data,
                                              scraped_data=scraped_data)
            filtered_urls = [{"url": url, "required_data": self.required_data} for url in filtered_urls]
            return filtered_urls, scraped_data
        else:
            return None, None

    @staticmethod
    def create_output(url: str, response: int, required_data: List[Dict], scraped_data: Dict[str, str]):
        return dict(url=url, required_data=required_data, response_code=response,
                    scraped_data=scraped_data)
