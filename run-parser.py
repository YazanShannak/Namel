import os
from distributed_crawler.logs.logger import Logger
from distributed_crawler.kafka.consumer import Consumer
from distributed_crawler.kafka.producer import Producer
from distributed_crawler.crawler.url_parser import UrlParser

hostname = os.environ.get("HOSTNAME")
parser_name = os.environ.get("node_name", hostname)
servers = ["kafka:9092"]

logger = Logger(name="url_parser")
consumer = Consumer(topic="domains", servers=servers, consumer_group="url_parsers", managed=True)
producer = Producer(topic="urls", node_name=parser_name, servers=servers)


def produce_url(url_object):
    """
    Logs and produces a new url object to kafka topic "urls"
    :param url_object: new url object to produce
    :type url_object: Dictionary of url and required_data
    """
    logger.log(url_object)
    producer.send_message(url_object)


while True:
    """
    Infinitely get one message at a time from the kafka topic "domains",
    instantiate a new UrlParser and crawls the urls, 
    produces an url_object each time its pushed to the stream 
    """
    message = consumer.get_message()
    domain_url = message["url"]
    domain_required_data = message["required_data"]
    logger.log("Received domain {} to crawl".format(domain_url))
    parser = UrlParser(domain_url=domain_url, required_data=domain_required_data)
    parser.parsed_urls.subscribe(on_next=produce_url)
    parser.start_crawl()
