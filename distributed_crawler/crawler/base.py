from typing import List, Dict, Tuple, Optional
import requests
from lxml import html
from urllib.parse import urljoin, urlsplit


class Base:
    def __init__(self, url: str, required_data: List[Dict]):
        self.url, self.required_data = url, required_data
        self.response_code, self.response_content = self.get_page(self.url)
        self.root = html.fromstring(self.response_content) if self.response_code == 200 else None
        self.domain_meta = urlsplit(self.url)

    @staticmethod
    def get_page(url: str) -> Tuple:
        """
        Perform an http request, returns content of the response
        :param url: url to get content for
        :type url: str
        :return: Content of the response from the url
        :rtype: bytes
        """
        # response = requests.get("http://splash:8050/render.json?url={}&html=1")
        response = requests.get(url=url)
        return response.status_code, response.content

    @staticmethod
    def get_url_netloc(url: str) -> str:
        """
        parse the netloc (domain) of the url
        :param url:
        :type url: str
        :return: netloc of the url
        :rtype: str
        """
        return urlsplit(url).netloc

    def handle_relative_url(self, new_url, main_url) -> str:
        """
        Check if the url is absolute or relative, and if relative construct an absolute url from its reference
        :param new_url: url to check and handle
        :type new_url: str
        :param main_url: the url where it was found (reference)
        :type main_url: str
        :return: absolute url oath with the proper domain from its reference
        :rtype: str
        """
        netloc = self.get_url_netloc(new_url)
        return new_url if netloc else urljoin(main_url, new_url)

    def parse_urls(self, url: str, page_content: bytes) -> Optional[List[str]]:
        """
        parse all urls from the page of a given url, handles relative paths (urls) and filters external urls
        :param url: url to parse urls from
        :type: url: str url
        :param page_content: response's content of the page to parse urls from, as returned by the requests package
        :type page_content: byes
        :return: List of urls in the page of the specified urls
        :rtype: List of str urls
        """
        new_urls = self.root.xpath("//a/@href")
        new_urls = [self.handle_relative_url(new_url=new_url, main_url=url) for new_url in new_urls]
        return self.filter_external_links(new_urls)

    def filter_external_links(self, urls):
        """
        filters external links from a list of links, the reference domain is the instance's domain_url
        :param urls: list of urls to filter
        :rtype: list of str urls
        :return: external links filtered list of urls from
        :rtype: list of str urls
        """
        urls_netlocs = [(url, self.get_url_netloc(url)) for url in urls]
        return [url for url, netloc in urls_netlocs if netloc == self.domain_meta.netloc]

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
