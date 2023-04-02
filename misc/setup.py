import psycopg2
import logging
import time

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

create_trading_table_query = '''
    CREATE TABLE trading (
        timestamp int PRIMARY KEY,
        min float,
        max float,
        avg float
    );
'''

create_comments_table_query = '''
    CREATE TABLE comments (
        id serial primary key,
        comment text,
        author_id int,
        timestamp int,
        FOREIGN KEY(author_id) 
	    REFERENCES authors(id)
    );
'''

create_authors_table_query = '''
    CREATE TABLE authors (
        id serial primary key,
        name varchar(255) unique
    );
'''

logging.basicConfig(filename='../setup.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

cur = conn.cursor()
try:
    cur.execute(create_authors_table_query)
    cur.execute(create_trading_table_query)
    cur.execute(create_comments_table_query)
    conn.commit()
    logging.info("Successfully created tables!")
except Exception as e:
    logging.error(f"{e}")
cur.close()
conn.close()
