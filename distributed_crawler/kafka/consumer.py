from .client import Client
import json
from typing import List


class Consumer(Client):
    def __init__(self, topic: str, consumer_group: str, servers: List[str] = None, managed: bool = True):
        if servers is None:
            super().__init__()
        else:
            super().__init__(servers)
        self.topic_name = topic
        self.topic = self.get_topic(self.client, self.topic_name)
        self.consumer_group = consumer_group
        self.managed = managed
        self.consumer = self.get_consumer()

    def get_consumer(self):
        return self.topic.get_balanced_consumer(consumer_group=self.consumer_group, managed=self.managed,
                                                auto_commit_enable=False)

    def get_message(self):
        message = self.consumer.consume()
        value, partition, offset = self.dict_from_binary(message.value), message.partition, message.offset
        self.consumer.commit_offsets([(partition, offset)])
        return value

    @staticmethod
    def dict_from_binary(binary):
        return json.loads(binary.decode("ascii"))
