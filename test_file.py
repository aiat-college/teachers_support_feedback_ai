import sqlite3

conn = sqlite3.connect("data/database.sqlite3")
cursor = conn.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM Notes_notes
WHERE School='Udavi'
AND Created_date BETWEEN '2022-06-01' AND '2022-07-30'
""")

print(cursor.fetchone())