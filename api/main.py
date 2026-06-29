from unittest import result
from backend.rag.query import (
    generate_teacher_feedback,
    extract_keywords,
    get_top_youtube_videos,
    youtube_index,
)
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "database.sqlite3"
app = FastAPI()



# -----------------------------
# 2. REQUEST BODY
# -----------------------------
class RequestModel(BaseModel):
    school: str
    start_date: str
    end_date: str


# -----------------------------
# 3. DATABASE CONNECTION
# -----------------------------


def get_db_connection():

    print("DB FILE:", DB_PATH)
    print("DB EXISTS:", DB_PATH.exists())

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn

# -----------------------------
# 4. FETCH DATA FROM DB
# -----------------------------
def fetch_teacher_entries(school, start_date, end_date):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        Username,
        School,
        Grade,
        What_I_prepared,
        What_I_did_well,
        What_went_well,
        Where_to_improve,
        Created_date,
        What_homework_did_I_give_today
    FROM Notes_notes
    WHERE LOWER(School) = LOWER(?)
    AND DATE(Created_date) BETWEEN DATE(?) AND DATE(?)
    """

    cursor.execute(
        query,
        (school, start_date, end_date)
    )

    rows = cursor.fetchall()

    print("School received:", school)
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Rows found:", len(rows))

    if rows:
        print(dict(rows[0]))

    conn.close()

    return rows
@app.post("/generate-feedback")
def generate_feedback(req: RequestModel):

    try:
        rows = fetch_teacher_entries(
            req.school,
            req.start_date,
            req.end_date
        )

        print("Rows found:", len(rows))

        if not rows:
            return {"message": "No teacher data found"}

        teacher_map = {}

        for r in rows:

            name = r["Username"]

            text = f"""
Grade: {r['Grade']}

Prepared:
{r['What_I_prepared']}

Did Well:
{r['What_I_did_well']}

Went Well:
{r['What_went_well']}

Needs Improvement:
{r['Where_to_improve']}

Homework:
{r['What_homework_did_I_give_today']}
"""

            if name not in teacher_map:
                teacher_map[name] = []

            teacher_map[name].append(text)

        results = []

        # Process each teacher
        for teacher, entries in teacher_map.items():

            notes_count = len(entries)

            teacher_text = "\n".join(entries)

            # Step 1
            feedback = generate_teacher_feedback(
                teacher,
                teacher_text,
                notes_count
            )

            # Step 2
            keywords = extract_keywords(feedback)

            # Step 3
            youtube_videos = get_top_youtube_videos(
                youtube_index,
                keywords
            )

            results.append({
                "teacher": teacher,
                "feedback": feedback,
                "youtube": youtube_videos
            })

        # <-- OUTSIDE the for loop
        response_data = {
            "results": results
        }

        return response_data

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "error": str(e)
        }