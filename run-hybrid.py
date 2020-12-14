import os
from redis import Redis
from redisbloom.client import Client
from distributed_crawler.logs.logger import Logger
from distributed_crawler.kafka.consumer import Consumer
from distributed_crawler.kafka.producer import Producer
from distributed_crawler.crawler.hybrid import Hybrid

hostname = os.environ.get("HOSTNAME")
scraper_name = os.environ.get("node_name", hostname)
servers = ["kafka:9092"]

logger = Logger(name="hybrid")
consumer = Consumer(topic="urls", servers=servers, consumer_group="workers", managed=True)
producer_data = Producer(topic="data", node_name=scraper_name, servers=servers)
producer_urls = Producer(topic="urls", node_name=scraper_name, servers=servers)
redis = Client(host="redis", port=6379)


def produce_scraped_data(data):
    """
    Logs and produces a new url object to kafka topic "urls"
    :param data: new data object to produce
    :type url_object: Dictionary of url, required_data and parsed_data
    """
    producer_data.send_message(data)


def produce_url(url_object):
    """
    Logs and produces a new url object to kafka topic "urls"
    :param url_object: new url object to produce
    :type url_object: Dictionary of url and required_data
    """
    logger.log(url_object)
    producer_urls.send_message(url_object)


while True:
    url_info = consumer.get_message()
    url, required_data = url_info.get("url"), url_info.get("required_data")
    logger.log("Received url {} to scrape".format(url))
    scraper = Hybrid(url=url, required_data=required_data, redis_client=redis)
    new_urls, data = scraper.crawl()
    if data:
        produce_scraped_data(data)
    if new_urls and len(new_urls) > 0:
        for url in new_urls:
            produce_url(url)
