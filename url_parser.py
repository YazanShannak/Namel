import os
from distributed_crawler.logs.logger import Logger
from distributed_crawler.kafka.consumer import Consumer
from distributed_crawler.kafka.producer import Producer
from distributed_crawler.crawler.url_parser import UrlParser

hostname = os.environ.get("HOSTNAME")
parser_name = os.environ.get("parser_name", hostname)

logger = Logger(name="url_parser")
# consumer = Consumer(topic="domains", servers=["localhost:29092"], consumer_group="url_parsers", managed=True)
# producer = Producer(topic="urls", node_name=parser_name, servers=["localhost:29092"])

parser = UrlParser(domain="http://books.toscrape.com")
parser.parsed_urls.subscribe(on_next=lambda x: print(x))
parser.crawl_all()
