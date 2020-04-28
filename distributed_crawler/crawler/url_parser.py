from urllib.parse import urljoin, urlsplit
import requests
from rx.subject import Subject
from lxml import html
from .entities import Domain, Url
from typing import List


class UrlParser:
    def __init__(self, domain: Domain):
        self.domain = domain
        self.domain_meta = urlsplit(self.domain.url)
        self.parsed_urls = Subject()
        self.parsed_pages = []

    @staticmethod
    def get_page(url: str):
        return requests.get(url).content

    @staticmethod
    def get_url_netloc(url):
        return urlsplit(url).netloc

    def handle_relative_url(self, url):
        split = urlsplit(url)
        if not split.netloc:
            return urljoin(self.domain.url, url)
        else:
            return url

    def parse_urls(self, url: str) -> List[str]:
        page = self.get_page(url)
        root = html.fromstring(page)
        urls = root.xpath("//a/@href")
        urls = [self.handle_relative_url(url) for url in urls]
        return self.filter_external_links(urls)

    def filter_external_links(self, urls):
        urls_netlocs = [(url, self.get_url_netloc(url)) for url in urls]
        return [url for url, netloc in urls_netlocs if netloc == self.domain_meta.netloc]

    def push_url(self, url: str):
        url = Url(url, self.domain.data)
        self.parsed_urls.on_next(url.object)

    def crawl_page(self, url):
        urls = self.parse_urls(url)
        self.parsed_pages.append(url)
        self.push_url(url)
        for url in urls:
            if url not in self.parsed_pages:
                self.crawl_page(url)

    def crawl_all(self):
        urls = self.parse_urls(self.domain.url)
        self.parsed_pages.append(self.domain.url)
        self.push_url(self.domain.url)
        for url in urls:
            self.crawl_page(url)
        self.parsed_urls.on_completed()
