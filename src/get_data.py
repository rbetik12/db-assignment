from clickhouse_driver import Client
from prettytable import PrettyTable
import matplotlib.pyplot as plt

# ClickHouse connection parameters
ch_host = 'localhost'
ch_port = 9000
ch_dbname = 'db'
ch_user = 'default'
ch_password = ''

# Connect to ClickHouse
conn = Client(host=ch_host, port=ch_port, database=ch_dbname, user=ch_user, password=ch_password)

# Get which comments user wrote while buying Apple Inc shares
query = 'select distinct author, text from comments c join deals d on author = d.person where d.share = \'Apple Inc.\' and d.action = 0'
res = conn.execute(query)
table = PrettyTable()
table.field_names = ["Author", "Text"]
table.add_rows(res)
print("Comments during Apple Inc shares purchasing")
print(table)

#Get how much money each user spent
query = 'select person, price, amount from deals'
res = conn.execute(query)
amount_by_person = {}
for (person, price, amount) in res:
    if person in amount_by_person:
        amount_by_person[person] += price * amount
    else:
        amount_by_person[person] = price * amount
amount_by_person = {k: v for k, v in sorted(amount_by_person.items(), key=lambda item: item[1], reverse=False)}
amounts = amount_by_person.values()
persons = amount_by_person.keys()

plt.xticks(rotation=90)
plt.bar(persons, amounts)
plt.title('User spendings')
plt.savefig("../logs/spendings.png")
plt.close()

#Get top-10 of the most popular shares by revenue
query = 'select price, amount, share from deals'
res = conn.execute(query)
shares_by_revenue = {}
for (price, amount, share) in res:
    if share in shares_by_revenue:
        shares_by_revenue[share] += price * amount
    else:
        shares_by_revenue[share] = price * amount
shares_by_revenue = {k: v for k, v in sorted(shares_by_revenue.items(), key=lambda item: item[1], reverse=False)}
amounts = list(shares_by_revenue.values())[-10:]
persons = list(shares_by_revenue.keys())[-10:]

plt.xticks(rotation=90)
plt.bar(persons, amounts)
plt.title('Top-10 shares by revenue')
plt.savefig("../logs/shares.png")