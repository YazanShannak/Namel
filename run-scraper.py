import os
from distributed_crawler.logs.logger import Logger
from distributed_crawler.kafka.consumer import Consumer
from distributed_crawler.kafka.producer import Producer
from distributed_crawler.crawler.data_scraper import DataScraper


hostname = os.environ.get("HOSTNAME")
scraper_name = os.environ.get("node_name", hostname)
servers = ["kafka:9092"]

logger = Logger(name="data_scraper")
consumer = Consumer(topic="urls", servers=servers, consumer_group="data_scrapers", managed=True)
producer = Producer(topic="items", node_name=scraper_name, servers=servers)


def produce_scraped_data(data):
    """
    Logs and produces a new url object to kafka topic "urls"
    :param data: new data object to produce
    :type url_object: Dictionary of url, required_data and parsed_data
    """
    producer.send_message(data)


while True:
    url_info = consumer.get_message()
    url_info = Url(url=url_info["url"], data=url_info["data"])
    logger.log("Received url {} to scrape".format(url_info.url))
    scraper = DataScraper(url=url_info)
    output = scraper.scrape_page()
    produce_scraped_data(output)
