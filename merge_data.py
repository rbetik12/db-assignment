import redis
import json
from pymongo import MongoClient
import psycopg2
import time
import logging

logging.basicConfig(filename='merge.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
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
        except psycopg2.OperationalError as e:
            time.sleep(3)


redis_keys = [key.decode() for key in redis_client.scan_iter(match='*', count=1024)]
redis_values = [json.loads(redis_client.get(key)) for key in redis_keys]
mongo_it = mongo_collection.find().sort('_id', -1).limit(1024)
mongo_values = [obj for obj in mongo_it]

for comment in mongo_values:
    try:
        cur = conn.cursor()
        insert_author_query = f'insert into authors (name) values (\'{comment["author"]}\')'
        cur.execute(insert_author_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(e)

    cur = conn.cursor()
    cur.execute(f'SELECT id FROM authors WHERE name = \'{comment["author"]}\'')
    author_id = cur.fetchone()[0]

    cur = conn.cursor()
    insert_comment_query = f'insert into comments (comment, author_id, timestamp) values (\'{comment["comment"]}\', {author_id}, {comment["timestamp"]})'
    cur.execute(insert_comment_query)
    conn.commit()

for value in redis_values:
    cur = conn.cursor()
    insert_value_query = f'insert into trading (timestamp, min, max, avg) values ({value["timestamp"]}, {value["min"]}, {value["max"]}, {value["avg"]})'
    cur.execute(insert_value_query)
    conn.commit()

logging.info("Succesfully merged data!")


