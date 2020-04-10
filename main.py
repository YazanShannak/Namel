from distributed_crawler.kafka.consumer import Consumer
import os
from distributed_crawler.logs.logger import Logger

parser_name = os.environ.get("parser_name")
consumer = Consumer("domains", consumer_group="url_parsers", servers=["kafka:9092"])
logger = Logger(name=parser_name)

while True:
    message = consumer.get_message()
    logger.log(
        "{} received message with offset:{} from partition: {} and value: {}".format(parser_name, message["offset"],
                                                                                     message["partition"],
                                                                                     message["message"]))
