from pymongo import MongoClient
import time
import logging
import random
from misc import utils
import json

class Comment:
    def __init__(self, text, timestamp):
        self.text = text
        self.timestamp = timestamp
        self.author = utils.get_random_name()

    @classmethod
    def create_random_comment(cls):
        text = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(10))
        timestamp = int(time.time())
        comment = cls(text, timestamp)

        return comment

    def to_dict(self):
        return {
            'text': self.text,
            'timestamp': self.timestamp,
            'author': self.author
        }

logging.basicConfig(filename='../logs/mongo.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
client = MongoClient('localhost', 27017)
db = client['db']
collection = db['comments']

print("Started gathering comments...")

while True:
    comment = Comment.create_random_comment()
    collection.insert_one(comment.to_dict())
    logging.info(json.dumps(comment.to_dict()))
    time.sleep(0.01)
