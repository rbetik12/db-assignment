import random
import math
import time
import redis
import logging
import json
from enum import Enum
from misc import utils

SAMPLES_PER_SECOND_AMOUNT = 1000


class Action(Enum):
    BUY = "Buy"
    SELL = "Sell"


class Deal:
    deal_id = int(time.time())

    def __init__(self, price, action, timestamp, amount):
        self.deal_id = Deal.deal_id
        Deal.deal_id += 1
        self.share = utils.get_random_share()
        self.price = price
        self.action = action
        self.person = utils.get_random_name()
        self.timestamp = timestamp
        self.amount = amount

    def to_dict(self):
        return {
            "deal_id": self.deal_id,
            "share": self.share,
            "price": self.price,
            "action": self.action.value,
            "person": self.person,
            "timestamp": str(self.timestamp),
            "amount": self.amount
        }


def create_random_deal():
    price = math.fabs(fn(round(random.uniform(1.0, 100.0), 2)))
    action = random.choice(list(Action))
    timestamp = int(time.time())
    amount = random.randint(10, 4096)
    deal = Deal(price, action, timestamp, amount)
    return deal


def fn(x: float) -> float:
    return math.sin(x) + float(random.randint(-10, 10))


logging.basicConfig(filename='logs/redis.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
r = redis.Redis(host='localhost', port=6379, db=0)

print("Started gathering trading data...")

while True:
    deal = create_random_deal()
    deal_json = json.dumps(deal.to_dict())
    logging.info(str(deal_json))
    r.set(deal.deal_id, deal_json)
    time.sleep(0.01)
