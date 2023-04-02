import psycopg2
import time
import binascii
from prettytable import PrettyTable

print("Connecting to PostgreSQL...")
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

cur = conn.cursor()
cur.execute("SELECT * FROM trading")
rows = cur.fetchall()

print("Trading data:")
table = PrettyTable()
table.field_names = ['timestamp', 'min', 'max', 'avg']
postgres_data = []
for row in rows:
    postgres_data.append(([row[0], row[1], row[2], row[3]]))
postgres_data.sort()
for row in postgres_data:
    table.add_row([row[0], row[1], row[2], row[3]])
print(table)

cur = conn.cursor()
cur.execute("SELECT * FROM comments")
rows = cur.fetchall()

print("Comments data:")
table = PrettyTable()
table.field_names = ['id', 'comment', 'author_id', 'timestamp']
postgres_data = []
for row in rows:
    postgres_data.append(([row[0], row[1], row[2], row[3]]))
postgres_data.sort()
for row in postgres_data:
    table.add_row([row[0], row[1], row[2], row[3]])
print(table)

cur = conn.cursor()
cur.execute("SELECT * FROM authors")
rows = cur.fetchall()

print("Authors data:")
table = PrettyTable()
table.field_names = ['id', 'name']
postgres_data = []
for row in rows:
    postgres_data.append(([row[0], row[1]]))
postgres_data.sort()
for row in postgres_data:
    table.add_row([row[0], row[1]])
print(table)

cur.close()
conn.close()