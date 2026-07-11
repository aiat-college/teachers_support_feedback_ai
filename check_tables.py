# check_tables.py

import sqlite3

db = r"C:\Users\Admin\OneDrive\Documents\GitHub\teachers_feedback\data\database.sqlite3"

conn = sqlite3.connect(db)

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

print(cursor.fetchall())

conn.close()