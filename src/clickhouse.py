import psycopg2
from clickhouse_driver import Client

# PostgreSQL connection parameters
pg_host = 'localhost'
pg_port = 5432
pg_dbname = 'db'
pg_user = 'kek'
pg_password = 'lolkek'

# ClickHouse connection parameters
ch_host = 'localhost'
ch_port = 9000
ch_dbname = 'db'
ch_user = 'default'
ch_password = ''

# Connect to PostgreSQL
pg_conn = psycopg2.connect(host=pg_host, port=pg_port, dbname=pg_dbname, user=pg_user, password=pg_password)
pg_cursor = pg_conn.cursor()

# Connect to ClickHouse
ch_conn = Client(host=ch_host, port=ch_port, database=ch_dbname, user=ch_user, password=ch_password)

# Move data from PostgreSQL to ClickHouse for deals table
pg_cursor.execute('SELECT * FROM deals')
deals_data = pg_cursor.fetchall()
ch_conn.execute('TRUNCATE TABLE deals')
ch_conn.execute('INSERT INTO deals (id, share, price, action, person, timestamp, amount) VALUES', deals_data)

# Move data from PostgreSQL to ClickHouse for comments table
pg_cursor.execute('SELECT * FROM comments')
comments_data = pg_cursor.fetchall()
ch_conn.execute('TRUNCATE TABLE comments')
ch_conn.execute('INSERT INTO comments (id, text, timestamp, author) VALUES', comments_data)

# Close connections
pg_cursor.close()
pg_conn.close()
ch_conn.disconnect()