import sqlite3
from collections import defaultdict

DB_PATH = "data/database.sqlite3"


def fetch_teacher_entries(
    school,
    start_date,
    end_date
):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM Notes_notes
        WHERE School = ?
        AND Created_date BETWEEN ? AND ?
        ORDER BY Username ASC
    """

    cursor.execute(
        query,
        (school, start_date, end_date)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def group_by_teacher(records):

    teachers = defaultdict(list)

    for row in records:

        teachers[row["Username"]].append(
            dict(row)
        )

    return teachers