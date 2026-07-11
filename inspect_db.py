import sqlite3

conn = sqlite3.connect("data/database.sqlite3")
cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print("TABLES FOUND:")
print(tables)

for table in tables:
    table_name = table[0]

    print("\n" + "=" * 50)
    print("TABLE:", table_name)
    print("=" * 50)

    cursor.execute(f"PRAGMA table_info({table_name})")

    columns = cursor.fetchall()

    for column in columns:
        print(column)

conn.close()