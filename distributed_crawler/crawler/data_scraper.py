from lxml import html
from typing import List, Dict
from .base import Base


class DataScraper(Base):
    """
    Class to scrape data from a given page
    """
    def __init__(self, url: str, required_data: List[Dict]):
        """
        :param url: url of the page to be scraped for the required data
        :type url: str url of the page
        :param required_data: required data to be looked for and parsed from the page
        :type required_data: list of objects, keys are "key" and "xpath"
        """
        super(DataScraper, self).__init__(url=url, required_data=required_data)
        self.scraped_data = None

    def create_output(self):
        """
        Creates an output dictionary from the scraping process
        :return: returns dictionary containing the final result from the scraper
        :rtype: dictionary with keys: url, required_data, response_code, scraped_data
        """
        return dict(url=self.url, required_data=self.required_data, response_code=self.response_code,
                    scraped_data=self.scraped_data)


    def scrape_page(self):
        """
        Scrapes required data from the page if we had a successful response from the url
        :return: returns dictionary containing the final result from the scraper
        rtype: dictionary with keys: url, required_data, response_code, parsed_data
        """
        if self.response_code == 200:
            scraped_data = self._scrape_data()
            self.scraped_data = scraped_data
        return self.create_output()
