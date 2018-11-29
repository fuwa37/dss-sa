import tweet
from flask import Flask, jsonify, request, render_template
import os
import fs

port = int(os.environ.get('PORT', 33507))
app = Flask(__name__)


def persentase(data, c):
    pos = float(0)
    neg = float(0)
    n = float(0)
    for i in data:
        if i['sentiment'] > 0:
            pos = pos + 1
        elif i['sentiment'] < 0:
            neg = neg + 1
        else:
            n = n + 1
    return (pos / c) * 100, (neg / c) * 100, (n / c) * 100


@app.route('/')
def main():
    return "a"


@app.route('/search')
def search():
    global c
    q = request.args.get("query")
    c = request.args.get("count")

    if c is None:
        c = 100
        data, sesi = tweet.analyzesearch(q)
    else:
        c = int(c)
        data, sesi = tweet.analyzesearch(q, c)

    pos, neg, n = persentase(data, c)
    return render_template("search.html", q=q, pos=pos, neg=neg, n=n, sesi=sesi)

@app.route('/session')
def session():
    data = []
    sesi = request.args.get("sesi")
    docs = fs.sesi_ref.document(sesi).collection("tweet").get()

    for doc in docs:
        data.append(doc.to_dict())

    return jsonify(data)

app.run(host='0.0.0.0', port=port)
