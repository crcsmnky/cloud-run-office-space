import os

from decimal import Decimal, ROUND_DOWN
from bson.json_util import dumps
from datetime import datetime
from flask import Flask, request, abort
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "7ad6b29a8134b52f54a96e276d38c7f1" # md5 -s "office space"

# app.config['MONGO_URI'] = 'mongodb://{host}:{port}/{database}'.format(
#     host=os.environ.get('MONGODB_HOST', 'mongodb'),
#     port=os.environ.get('MONGODB_PORT', 27017),
#     database=os.environ.get('MONGODB_DB', 'officespace')
# )

app.config['MONGO_URI'] = 'mongodb://mongodb:27017/officespace'

mongo = PyMongo(app)


@app.route('/compute', methods=['GET'])
def compute():
    amount = int(request.args.get('amount', None))
    rate = float(request.args.get('rate', None))

    if not amount or not rate:
        abort(404)

    tot = (amount * rate) + amount
    txn = float(str(Decimal(tot).quantize(Decimal('.01'), rounding=ROUND_DOWN)))
    rem = tot - txn

    banktxn = {
        'date': datetime.now(),
        'amount': txn
    }

    mongo.db.bank.insert(banktxn)

    usertxn = {
        'date': datetime.now(),
        'amount': rem
    }

    mongo.db.accounts.insert(usertxn)

    return 'ok', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6000))
    app.run(host='127.0.0.1', port=port, debug=False)



