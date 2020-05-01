from flask_restful import Resource
from flask import request
import json

dummy_jobs = [
    {"id": 1, "domain": "http://books.toscrape.com", "data": [{"key": "title", "xpath": "//h1[@class='title']"}]}
]


class DomainJob(Resource):
    def __init__(self, **kwargs):
        self.producer = kwargs.get("producer")

    def get(self):
        return {"jobs": dummy_jobs}

    def post(self):
        payload = request.get_json(force=True)
        url, data = payload["url"], payload["data"]
        obj = {"url": url, "data": data}
        message = json.dumps(obj).encode()
        self.producer.produce(message)
        return obj
