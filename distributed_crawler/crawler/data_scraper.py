from lxml import html
import requests
from typing import List, Dict


class DataScraper:
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
        self.url = url
        self.required_data = required_data
        self.page_content, self.response_code = self.get_page(self.url)
        self.root = html.fromstring(self.page_content) if self.response_code == 200 else None
        self.scraped_data = None

    @staticmethod
    def get_page(url: str):
        """
        Perform an http request, returns content of the response
        :param url: url to get content for
        :type url: str
        :return: Content of the response from the url
        :rtype: bytes
        """
        response = requests.get(url)
        return response.content, response.status_code

    def create_output(self):
        """
        Creates an output dictionary from the scraping process
        :return: returns dictionary containing the final result from the scraper
        :rtype: dictionary with keys: url, required_data, response_code, scraped_data
        """
        return dict(url=self.url, required_data=self.required_data, response_code=self.response_code,
                    scraped_data=self.scraped_data)

    def _scrape_data(self):
        """
        Parse the required data from the page if it exists
        :return: Returns a dictionary with the output data from the page if exists, else None
        :rtype: dictionary with keys: key, data or None
        """
        output = []
        for data_item in self.required_data:
            key, xpath = data_item.get("key"), data_item.get("xpath")
            result = self.root.xpath(xpath)
            if result:
                result = result[0] if len(result) == 1 else result
                new_item = dict(key=key, data=result)
                output.append(new_item)
        return output if len(output) > 0 else None

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
