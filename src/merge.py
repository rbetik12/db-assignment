import redis
import json
from pymongo import MongoClient
import psycopg2
import time
import logging
import datetime


def convert_timestamp_ms_to_postgres(timestamp_ms, is_correct=False):
    if is_correct:
        timestamp_dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000)
    else:
        timestamp_dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000)
    timestamp_str = timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')
    # timestamp_postgres = f"to_timestamp('{timestamp_str}', 'YYYY-MM-DD HH:MI:SS')"
    # return timestamp_postgres
    return timestamp_str


logging.basicConfig(filename='logs/merge.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
redis_client = redis.Redis(host='localhost', port=6379, db=0)
mongo_client = MongoClient('mongodb://localhost:27017/')

mongo_db = mongo_client['db']
mongo_collection = mongo_db['comments']

conn = None
for i in range(5):
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='db',
            user='kek',
            password='lolkek'
        )
        logging.info("Connected to PostgreSQL successfully")
        break
    except psycopg2.OperationalError as e:
        logging.error(str(e))
        time.sleep(3)

redis_keys = [key.decode() for key in redis_client.scan_iter(match='*', count=1024)]
redis_values = [json.loads(redis_client.get(key)) for key in redis_keys]
mongo_it = mongo_collection.find().sort('_id', -1).limit(1024)
mongo_values = [obj for obj in mongo_it]

for comment in mongo_values:
    try:
        cur = conn.cursor()
        insert_comment_query = f'insert into comments (text, timestamp, author) values (\'{comment["text"]}\', \'{convert_timestamp_ms_to_postgres(int(comment["timestamp"]) / 10**6)}\', \'{comment["author"]}\')'
        cur.execute(insert_comment_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(e)

for value in redis_values:
    try:
        cur = conn.cursor()
        insert_deal_query = f'insert into deals (id, share, price, action, person, timestamp, amount) values ({value["deal_id"]}, \'{value["share"]}\', {value["price"]}, {0 if value["action"] == "Sell" else 1}, \'{value["person"]}\', \'{convert_timestamp_ms_to_postgres(int(value["timestamp"]), True)}\', {value["amount"]})'
        cur.execute(insert_deal_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(e)
conn.close()
