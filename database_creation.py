import os
import sqlite3

conn = sqlite3.connect('database.sqlite')
print("Database path:", os.path.abspath('database.sqlite'))
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS reference (
        Timestamp DATETIME,
        Source_MAC TEXT,
        Destination_MAC TEXT,
        RSSI INTEGER,
        Distance REAL
        Location INTEGER
    )
''')

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in the database:", cursor.fetchall())
conn.commit()
conn.close()