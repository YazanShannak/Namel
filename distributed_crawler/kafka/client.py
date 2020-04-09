from pykafka import KafkaClient


class Client:
    def __init__(self, bootstrap_severs=['kafka:9092']):
        self.servers = bootstrap_severs
        self.client = self.create_client()

    def create_client(self):
        hosts = ",".join(self.servers)
        return KafkaClient(hosts=hosts)

    @staticmethod
    def get_topic(client, topic_name):
        return client.topics[topic_name]
