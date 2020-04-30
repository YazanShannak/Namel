from flask import Flask, render_template
from flask import request
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def add_domain():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
