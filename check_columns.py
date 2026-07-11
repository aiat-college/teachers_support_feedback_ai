import sqlite3

db = r"data/database.sqlite3"

conn = sqlite3.connect(db)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(Notes_notes)")

for row in cursor.fetchall():
    print(row)

conn.close()