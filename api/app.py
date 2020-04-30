from flask import Flask
from flask_restful import Api
from .resources.domain_job import DomainJob

app = Flask(__name__)
api = Api(app=app)

api.add_resource(DomainJob, '/domains')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
