from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
import requests
from rx.subject import Subject


class UrlParser:
    def __init__(self, domain: str):
        self.domain = domain
        self.domain_netloc = self.get_url_netloc(self.domain)
        self.parsed_urls = Subject()
        self.parsed_pages = []

    @staticmethod
    def get_page(url):
        return requests.get(url).content

    @staticmethod
    def get_url_netloc(url):
        return urlsplit(url).netloc

    def parse_urls(self, url):
        page = self.get_page(url)
        soup = BeautifulSoup(page, features='html.parser')
        urls = [a['href'] if a['href'].startswith("http") else urljoin(url, a['href']) for a in
                soup.find_all("a", href=True)]
        return self.filter_external_links(urls)

    def filter_external_links(self, urls):
        urls_netlocs = [(url, self.get_url_netloc(url)) for url in urls]
        return [url for url, netloc in urls_netlocs if netloc == self.domain_netloc]

    def crawl_page(self, url):
        urls = self.parse_urls(url)
        self.parsed_pages.append(url)
        self.parsed_urls.on_next(url)
        for url in urls:
            if url not in self.parsed_pages:
                self.crawl_page(url)

    def crawl_all(self):
        urls = self.parse_urls(self.domain)
        self.parsed_pages.append(self.domain)
        self.parsed_urls.on_next(self.domain)
        for url in urls:
            self.crawl_page(url)
