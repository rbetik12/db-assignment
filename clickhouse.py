import psycopg2
from clickhouse_driver import Client

conn = psycopg2.connect(
    host="localhost",
    database="db",
    user="kek",
    password="lolkek")

cur = conn.cursor()
cur.execute("SELECT * FROM authors")
authors_rows = cur.fetchall()

cur = conn.cursor()
cur.execute("SELECT * FROM comments")
comments_rows = cur.fetchall()

client = Client(host='locahost', port=9000, user='default', password='')

create_table_query = '''
CREATE TABLE IF NOT EXISTS authors (
    id Int32,
    name String,
    value Float32
) ENGINE = Memory
'''

client.execute(create_table_query)