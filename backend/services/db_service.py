import sqlite3

DB_PATH = "data/database.sqlite3"

def get_teacher_notes(school, start_date, end_date):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        Username,
        What_I_prepared,
        What_I_did_well,
        What_went_well,
        Where_to_improve,
        What_homework_did_I_give_today,
        Created_date
    FROM Notes_notes
    WHERE School = ?
      AND Created_date BETWEEN ? AND ?
    ORDER BY Username, Created_date
    """, (school, start_date, end_date))

    rows = cursor.fetchall()

    conn.close()

    return rows