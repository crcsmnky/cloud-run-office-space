import os
import requests
import random
import time

COMPUTE_API = '{host}'.format(
    host=os.environ.get('COMPUTE_API', 'http://localhost:6000'),
)

def generate():

    batch = int(os.environ.get('BATCH_SIZE', 10))
    min_amount = int(os.environ.get('MIN_AMOUNT', 1))
    max_amount = int(os.environ.get('MAX_AMOUNT', 1000))
    rate = float(os.environ.get('INTEREST_RATE', .0375))

    txn_amounts = random.sample(range(min_amount, max_amount), batch)

    try:
        for amount in txn_amounts:
            txn = {
                'amount': amount,
                'rate': rate
            }
            ret = requests.post(COMPUTE_API + '/compute', data = txn)
            time.sleep(1)
    except Exception as e:
        print(f'error: {e}')


if __name__ == '__main__':
    print(f'using COMPUTE_API ==> {COMPUTE_API}/compute')

    while True:
        generate()