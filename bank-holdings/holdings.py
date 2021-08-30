import os

from flask import Flask, request, render_template
from google.cloud import firestore

app = Flask(__name__)
app.secret_key = "7ad6b29a8134b52f54a96e276d38c7f1" # md5 -s "office space"

db = firestore.Client()

BANK = os.environ.get('BANK_COLLECTION', 'holdings')

@app.route("/", methods=['GET'])
def balance():
    txn_stream = db.collection(BANK).order_by(
        'date', direction=firestore.Query.DESCENDING).limit(10).stream()

    total = 0
    txns = list()

    for txn in txn_stream:
        txns.append(txn.to_dict())
        total += txn.get('amount')

    return render_template('holdings.html', txns=txns, total=total)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
