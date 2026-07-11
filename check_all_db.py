import sqlite3
from pathlib import Path

dbs = [
    "database.sqlite3",
    "data/database.sqlite3",
    "teachers.db",
    "backend/db/teacher_input_db.db",
    "backend/db/teacher_input_db.sqlite3",
]

for db in dbs:
    path = Path(db)

    if path.exists():
        print(f"\n===== {path} =====")

        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """)

        for table in cursor.fetchall():
            print(table[0])

        conn.close()