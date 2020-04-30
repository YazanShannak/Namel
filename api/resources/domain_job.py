from flask_restful import Resource

dummy_jobs = [
    {"id": 1, "domain": "http://books.toscrape.com", "data": [{"key": "title", "xpath": "//h1[@class='title']"}]}]


class DomainJob(Resource):
    def get(self):
        return {"jobs": dummy_jobs}
