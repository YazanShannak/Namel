from .kafka.consumer import Consumer
import os

parser_name = os.environ.get("parser_name")

consumer = Consumer("domains", consumer_group="url_parsers")

while True:
    message = consumer.get_message()
    print("{} received message with offset:{} from partition: {} and value: {}".format(parser_name, message.offset,
                                                                                       message.parition,
                                                                                       message.message))
