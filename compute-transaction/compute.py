import os

from decimal import Decimal, ROUND_DOWN
from datetime import datetime
from flask import Flask, request

from google.cloud import firestore
from google.cloud import pubsub_v1 as pubsub

app = Flask(__name__)
app.secret_key = "7ad6b29a8134b52f54a96e276d38c7f1" # md5 -s "office space"

db = firestore.Client()

BANK = os.environ.get('BANK_COLLECTION', 'holdings')
ACCT = os.environ.get('ACCT_COLLECTION', 'account')

PROJECT = os.environ.get('PROJECT_ID')
TOPIC = os.environ.get('TOPIC_ID')

publisher = pubsub.PublisherClient()
topic_path = publisher.topic_path(PROJECT, TOPIC)

@app.route('/compute', methods=['POST'])
def compute():
    amount = int(request.form['amount'])
    rate = float(request.form['rate'])

    bug = os.environ.get('BUG', None)

    if bug is None:
        tot = (amount * rate) + amount
    else:
        tot = amount * rate

    txn = float(str(Decimal(tot).quantize(Decimal('.01'), rounding=ROUND_DOWN)))
    rem = tot - txn

    banktxn = {
        'date': datetime.now(),
        'amount': txn
    }
    db.collection(BANK).add(banktxn)

    accttxn = {
        'date': datetime.now(),
        'amount': rem
    }
    db.collection(ACCT).add(accttxn)

    msg = str(rem).encode('utf-8')
    future = publisher.publish(topic_path, msg)

    return 'added', 201


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=False)



