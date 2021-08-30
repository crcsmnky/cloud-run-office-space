import os
import base64
import redis 
import json

from flask import Flask, request, render_template
from google.cloud import firestore

app = Flask(__name__)
app.secret_key = "7ad6b29a8134b52f54a96e276d38c7f1" # md5 -s "office space"

db = firestore.Client()

ACCT = os.environ.get('ACCT_COLLECTION', 'account')

rhost = os.environ.get('REDIS_HOST', 'localhost')
rport = int(os.environ.get('REDIS_PORT', 6379))
cache = redis.Redis(host=rhost, port=rport) 


@app.route("/return-balance", methods=['GET'])
def balance():
    total = float(cache.get('total-balance'))
    txns = list()
    txn_stream = db.collection(ACCT).order_by(
        'date', direction=firestore.Query.DESCENDING).limit(10).stream()

    for txn in txn_stream:
        txns.append(txn.to_dict())

    return render_template('balance.html', txns=txns, total=total)


@app.route("/update-balance", methods=["POST"])
def update_balance():
    msg = json.loads(request.form['message'])
    amount = float(base64.b64decode(msg['data']).decode('utf-8').strip())
    cache.incrbyfloat('total-balance', amount)
    return 'ok', 200


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
