import sqlite3
import os

DB_PATH = "backend/db/teacher_input_db.db"

# Ensure folder exists
os.makedirs("backend/db", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS teacher_feedback_input (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    subject TEXT NOT NULL,
    class TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully")
