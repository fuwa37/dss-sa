import tweet
from flask import Flask, jsonify, request
import os

port = int(os.environ.get('PORT', 33507))
app = Flask(__name__)


@app.route('/')
def main():
    return "a"


@app.route('/search')
def search():
    q = request.args.get("query")
    c = request.args.get("count")
    if c is None:
        data = tweet.analyzesearch(q)
    else:
        c = int(c)
        data = tweet.analyzesearch(q, c)
    return jsonify(data)


app.run(host='0.0.0.0', port=port)