import os
import pymongo

from flask import Flask, request, render_template
from google.cloud import firestore

app = Flask(__name__)
app.secret_key = "7ad6b29a8134b52f54a96e276d38c7f1" # md5 -s "office space"

db = firestore.Client()

ACCT = os.environ.get('ACCT_COLLECTION', 'account')

@app.route("/", methods=['GET'])
def balance():
    txn_stream = db.collection(ACCT).order_by(
        'date', direction=firestore.Query.DESCENDING).stream()

    total = 0
    txns = list()

    for txn in txn_stream:
        txns.add(txn.to_dict())
        total += txn['amount']

    return render_template('balance.html', txns=txns, total=total)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=False)
