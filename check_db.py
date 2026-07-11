import sqlite3

conn = sqlite3.connect("data/database.sqlite3")
cursor = conn.cursor()

cursor.execute("""
SELECT Username, School, Created_date
FROM Notes_notes
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)

conn.close()