from flask import Flask
from flask_restful import Api
from .resources.domain_job import DomainJob
from pykafka import KafkaClient

client = KafkaClient(hosts="localhost:29092")
topics = client.topics
domains = topics['urls']
domains_producer = domains.get_producer()

app = Flask(__name__)
api = Api(app=app)

api.add_resource(DomainJob, '/domains', resource_class_kwargs={"producer": domains_producer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
