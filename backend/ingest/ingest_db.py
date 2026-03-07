# backend/ingest/ingest_db.py
import sqlite3

def ingest_teachernotes_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT teacher_name, question, response
        FROM feedback
    """)

    docs = []
    for t, q, r in cursor.fetchall():
        docs.append(
            f"Teacher {t} feedback: {q} rated {r}"
        )

    conn.close()
    return docs
