import os
from distributed_crawler.logs.logger import Logger
from distributed_crawler.kafka.consumer import Consumer
from distributed_crawler.kafka.producer import Producer
from distributed_crawler.crawler.url_parser import UrlParser

hostname = os.environ.get("HOSTNAME")
# parser_name = os.environ.get("parser_name", hostname)
parser_name = "Test Node"

logger = Logger(name="url_parser")
consumer = Consumer(topic="domains", servers=["localhost:29092"], consumer_group="url_parsers", managed=True)
producer = Producer(topic="urls", node_name=parser_name, servers=["localhost:29092"])


def produce_url(url):
    logger.log(url)
    producer.send_message({"url": url})


while True:
    message = consumer.get_message()
    domain = message['message']['url']
    parser = UrlParser(domain=domain)
    parser.parsed_urls.subscribe(on_next=produce_url)
    parser.crawl_all()