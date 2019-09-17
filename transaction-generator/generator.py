import os
import requests
import random
import time

from flask import Flask, request, render_template, flash

app = Flask(__name__)
app.secret_key = '7ad6b29a8134b52f54a96e276d38c7f1' # md5 -s 'office space'

API = 'http://{host}'.format(
    host=os.environ.get('API', 'localhost:6000'),
)

@app.route('/', methods=['GET', 'POST'])
def home():
    print 'using {api}'.format(api=API)
    
    if request.method == 'POST':
        count = int(request.form['txn_count'])
        min_amt = int(request.form['txn_minamt'])
        max_amt = int(request.form['txn_maxamt'])
        rate = float(request.form['txn_rate'])

        amounts = random.sample(xrange(min_amt, max_amt), count)

        try:
            for a in amounts:
                ret = requests.get(API + '/compute?amount={amount}&rate={rate}'.format(
                    amount=a, rate=rate))
                time.sleep(0.1)
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
        finally:
            flash('Generated {} transactions'.format(count), 'success')

    return render_template('generator.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=False)