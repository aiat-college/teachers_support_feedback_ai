from mentor_feedback.database import (
    fetch_teacher_entries,
    group_by_teacher
)

from backend.pipeline.query import run_query


def generate_feedback(school, start_date, end_date):

    records = fetch_teacher_entries(school, start_date, end_date)
    teachers = group_by_teacher(records)

    results = []

    for teacher_name, entries in teachers.items():

        teacher_text = ""

        for row in entries:
            teacher_text += f"""
Teacher Entry:

What I prepared:
{row['What_I_prepared']}

What I did well:
{row['What_I_did_well']}

What went well:
{row['What_went_well']}

Where to improve:
{row['Where_to_improve']}

Homework:
{row['What_homework_did_I_give_today']}

---
"""

        # 🔥 RAG CALL
        feedback = run_query(
            f"""
You are an expert teaching mentor.

Analyze the following teacher records and provide constructive feedback:

{teacher_text}

Give:
- Strengths
- Weaknesses
- Suggestions for improvement
- Overall summary
"""
        )

        results.append({
            "teacher": teacher_name,
            "feedback": feedback
        })

    return results