from typing import List, Dict
from urllib.parse import urlsplit
from .base import Base
from rx.subject import Subject


class UrlParser(Base):
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
        super(UrlParser, self).__init__(url=domain_url, required_data=required_data)
        self.domain_meta = urlsplit(self.url)
        self.parsed_urls = Subject()
        self.parsed_pages = []

    def push_url(self, url: str):
        """
        Publish a new parsed urls to the stream of parsed_urls subject
        :param url: url to add to parsed_urls stream
        :type url: str url
        """
        url_object = {"url": url, "required_data": self.required_data}
        self.parsed_urls.on_next(url_object)

    def crawl_page(self, url):
        """ TODO check and reimplement this method, try to check if the url is parsed too before parsing urls from """
        """
        Finds all urls in the page of the given url, then follows recursively until all urls are parsed
        :param url: recursively finds urls in the specified page and links to other pages
        """
        self.parsed_pages.append(url)
        code, content = self.get_page(url=url)
        if code == 200:
            urls = self.parse_urls(url=url, page_content=content)
            self.push_url(url)
            for url in urls:
                if url not in self.parsed_pages:
                    self.crawl_page(url)
        else:
            pass

    def start_crawl(self):
        """
        Crawls all pages in the domain recursively to find urls for all pages,
        the domain page is handled before the others
        """
        homepage_status, homepage_content = self.get_page(self.url)
        if homepage_status == 200:
            urls = self.parse_urls(url=self.url, page_content=homepage_content)
            self.parsed_pages.append(self.url)
            self.push_url(self.url)
            for url in urls:
                self.crawl_page(url)
            self.parsed_urls.on_completed()
        else:
            self.parsed_urls.on_error(Exception())
