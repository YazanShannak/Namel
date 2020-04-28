import os
from distributed_crawler.logs.logger import Logger
from distributed_crawler.kafka.consumer import Consumer
from distributed_crawler.kafka.producer import Producer
from distributed_crawler.crawler.data_scraper import DataScraper
from distributed_crawler.crawler.entities import Domain

hostname = os.environ.get("HOSTNAME")
parser_name = os.environ.get("parser_name", hostname)
servers = ["kafka:9092"]

logger = Logger(name="data_scraper")
consumer = Consumer(topic="urls", servers=servers, consumer_group="data_scrapers", managed=True)
producer = Producer(topic="items", node_name=parser_name, servers=servers)


def produce_data(data):
    pass


# logger.log(url)
# producer.send_message({"url": url})


while True:
    message = consumer.get_message()
    domain = Domain(message)
    logger.log("Received url {} to scrape".format(domain.url))
    scraper = DataScraper(url=domain.url, required_data=domain.data)
