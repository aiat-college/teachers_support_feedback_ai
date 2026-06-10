import sqlite3

DB_PATH = "backend/db/teacher_input_db.db"


def save_teacher_input(question, subject, class_name, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teacher_feedback_input
        (question, subject, class, category)
        VALUES (?, ?, ?, ?)
    """, (question, subject, class_name, category))

    conn.commit()
    conn.close()


def get_latest_teacher_input():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows dict-style access
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, question, subject, class, category
        FROM teacher_feedback_input
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row["id"],
        "question": row["question"],
        "subject": row["subject"],
        "class": row["class"],
        "category": row["category"]
    }
