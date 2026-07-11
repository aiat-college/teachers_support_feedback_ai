import sqlite3

conn = sqlite3.connect("data/database.sqlite3")
cursor = conn.cursor()

cursor.execute("""
SELECT
    Username,
    School,
    Created_date,
    What_I_did_well
FROM Notes_notes
WHERE School='Udavi'
ORDER BY Username
LIMIT 20
""")

for row in cursor.fetchall():
    print(row)

conn.close()