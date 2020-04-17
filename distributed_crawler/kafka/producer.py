from distributed_crawler.kafka.client import Client
from typing import List
import json


class Producer(Client):
    def __init__(self, topic: str, node_name: str, servers: List[str] = None):
        super().__init__() if servers is None else super().__init__(servers)
        self.topic_name = topic
        self.topic = self.get_topic(self.client, self.topic_name)
        self._producer = self.get_producer()
        self.node_name = node_name

    def get_producer(self):
        return self.topic.get_producer()

    def send_message(self, message):
        message["node_name"] = self.node_name
        message = self.dict_to_bytes(message)
        self._producer.produce(message)

    @staticmethod
    def dict_to_bytes(message: dict):
        return json.dumps(message).encode()
