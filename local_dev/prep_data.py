
import sqlite3

db = '../tickets.db'

query = open('local_dev/data_prep.sql', 'r').read()

conn = sqlite3.connect(db)

cursor = conn.cursor()

cursor.executescript(query)
