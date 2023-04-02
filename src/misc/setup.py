import psycopg2
import logging
import time

logging.basicConfig(filename='logs/setup.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

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

create_trading_data_table_query = '''
    CREATE TABLE deals (
        id int primary key,
        share varchar(255),
        price float,
        action int,
        person varchar(255),
        timestamp date,
        amount int
    );
'''

create_comments_table_query = '''
    CREATE TABLE comments (
        id serial primary key,
        text text,
        timestamp date,
        author varchar(255)
    );
'''


cur = conn.cursor()
try:
    cur.execute(create_trading_data_table_query)
    cur.execute(create_comments_table_query)
    conn.commit()
    logging.info("Successfully created trading data table")
except Exception as e:
    logging.error(f"{e}")
cur.close()
conn.close()
