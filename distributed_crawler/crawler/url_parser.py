from urllib.parse import urljoin, urlsplit
import requests
from rx.subject import Subject
from lxml import html
from typing import List, Dict


class UrlParser:
    """
    Class to asynchronously parse all urls from a given domain
    :param domain_url: Domain's URL to crawl
    :type domain_url: str
    :param domain_meta: Meta data from splitting domain_url
    :param parsed_urls: Stream of parsed urls
    :type parsed_urls: Subject of
    """

    def __init__(self, domain_url: str, required_data: List[Dict]):
        """
        Class to asynchronously parse all urls from a given domain
        :param domain_url: Domain's URL to crawl
        :type domain_url: str
        :param domain_meta: Meta data from splitting domain_url
        :param parsed_urls: Stream of parsed urls
        :type parsed_urls: Subject of
        """
        self.domain_url = domain_url
        self.required_data = required_data
        self.domain_meta = urlsplit(self.domain_url)
        self.parsed_urls = Subject()
        self.parsed_pages = []

    @staticmethod
    def get_page(url: str) -> bytes:
        """
        Perform an http request, returns content of the response
        :param url: url to get content for
        :type url: str
        :return: Content of the response from the url
        :rtype: bytes
        """
        return requests.get(url).content

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

    def parse_urls(self, url: str) -> List[str]:
        """
        parse all urls from the page of a given url, handles relative paths (urls) and filters external urls
        :param url: url to parse urls from
        :type: url: str url
        :return: List of urls in the page of the specified urls
        :rtype: List of str urls
        """
        page = self.get_page(url)
        root = html.fromstring(page)
        new_urls = root.xpath("//a/@href")
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

    def push_url(self, url: str):
        """
        Publish a new parsed urls to the stream of parsed_urls subject
        :param url: url to add to parsed_urls stream
        :type url: str url
        """
        url_object = {"url": url, "required_data": self.required_data}
        self.parsed_urls.on_next(url_object)

    def crawl_page(self, url):
        """TODO check and reimplement this method, try to check if the url is parsed too before parsing urls from """
        """
        Finds all urls in the page of the given url, then follows recursively until all urls are parsed
        :param url: recursively finds urls in the specified page and links to other pages
        """
        urls = self.parse_urls(url)
        self.parsed_pages.append(url)
        self.push_url(url)
        for url in urls:
            if url not in self.parsed_pages:
                self.crawl_page(url)

    def start_crawl(self):
        """
        Crawls all pages in the domain recursively to find urls for all pages,
        the domain page is handled before the others
        """
        urls = self.parse_urls(self.domain_url)
        self.parsed_pages.append(self.domain_url)
        self.push_url(self.domain_url)
        for url in urls:
            self.crawl_page(url)
        self.parsed_urls.on_completed()
