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
    CREATE TABLE if not exists deals (
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
    CREATE TABLE if not exists comments (
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

from clickhouse_driver import Client

ch_host = 'localhost'
ch_port = 9000
ch_user = 'default'
ch_password = ''

# Connect to ClickHouse
ch_conn = Client(host=ch_host, port=ch_port, user=ch_user, password=ch_password)

ch_create_trading_data_table_query = '''
    CREATE TABLE IF NOT EXISTS deals (
        id int,
        share varchar(255),
        price float,
        action int,
        person varchar(255),
        timestamp date,
        amount int,
        primary key(id)
    ) ENGINE = MergeTree();
'''

ch_create_comments_table_query = '''
    CREATE TABLE IF NOT EXISTS comments (
        id Int32,
        text text,
        timestamp date,
        author varchar(255),
        primary key(id)
    ) ENGINE = MergeTree();
'''

# Create database
ch_conn.execute('CREATE DATABASE IF NOT EXISTS db')
ch_conn.execute('use db')
ch_conn.execute(ch_create_trading_data_table_query)
ch_conn.execute(ch_create_comments_table_query)

# Close connection
ch_conn.disconnect()
