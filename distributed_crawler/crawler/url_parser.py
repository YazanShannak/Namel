from typing import List, Dict, Optional
from urllib.parse import urljoin, urlsplit

from lxml import html
from rx.subject import Subject

from .base import Base


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
        root = html.fromstring(page_content)
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
