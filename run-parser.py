import os
from distributed_crawler.logs.logger import Logger
from distributed_crawler.kafka.consumer import Consumer
from distributed_crawler.kafka.producer import Producer
from distributed_crawler.crawler.url_parser import UrlParser
from distributed_crawler.crawler.entities import Domain

hostname = os.environ.get("HOSTNAME")
parser_name = os.environ.get("parser_name", hostname)
servers = ["kafka:9092"]

logger = Logger(name="url_parser")
consumer = Consumer(topic="domains", servers=servers, consumer_group="url_parsers", managed=True)
producer = Producer(topic="urls", node_name=parser_name, servers=servers)


def produce_url(url):
    logger.log(url)
    producer.send_message(url)


while True:
    message = consumer.get_message()
    domain = Domain(message)
    logger.log("Received domain {} to crawl".format(domain.url))
    parser = UrlParser(domain=domain)
    parser.parsed_urls.subscribe(on_next=produce_url)
    parser.crawl_all()
