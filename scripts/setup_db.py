import sqlite3

conn = sqlite3.connect('lib/db/database.db')
cursor = conn.cursor()

with open('lib/db/schema.sql') as file:
    schema = file.read()
    cursor.executescript(schema)

conn.commit()
conn.close()

print("Database setup complete")
