import os
import pymongo

from flask import Flask, request, render_template
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


@app.route("/", methods=['GET'])
def balance():
    txns = mongo.db.accounts.find({}).sort([
        ('date', pymongo.DESCENDING)
    ]).limit(50)

    ops = [{
        '$group': {
            '_id': 'michaelbolton',
            'total': {
                '$sum': '$amount'
            }
        }
    }]
    tot = list(mongo.db.accounts.aggregate(ops))[0]

    return render_template('balance.html', txns=list(txns), total=round(tot['total'], 3))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=False)
