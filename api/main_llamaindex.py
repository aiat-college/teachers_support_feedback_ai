from fastapi import FastAPI

from api.models import RequestModel
from api.teacher_master import load_teacher_master

# from backend.pipeline.scraper import fetch_teacher_notes
from backend.rag.query_llamaindex import generate_teacher_feedback
from backend.pipeline.scraper import fetch_teacher_notes

from backend.services.teacher_notes_service import (
    TeacherNotesService
)

import traceback
import time

app = FastAPI()

service = TeacherNotesService()

# ------------------------------------
# Grade Normalization Function

# ------------------------------------
def normalize_grade(grade):
    grade = str(grade).strip().lower()

    mapping = {
        "1": "1st",
        "1st": "1st",
        "2": "2nd",
        "2nd": "2nd",
        "3": "3rd",
        "3rd": "3rd",
        "4": "4th",
        "4th": "4th",
        "5": "5th",
        "5th": "5th",
        "6": "6th",
        "6th": "6th",
        "7": "7th",
        "7th": "7th",
        "8": "8th",
        "8th": "8th",
        "9": "9th",
        "9th": "9th",
        "10": "10th",
        "10th": "10th",
        "nios": "NIOS"
    }

    return mapping.get(grade, grade)


@app.post("/generate-feedback")
def generate_feedback(req: RequestModel):

    print("========== API CALLED ==========")
    print(req)

    try:

        # -------------------------------------------------------
        # Fetch Teacher Notes
        # -------------------------------------------------------
        
        # rows = fetch_teacher_notes(
        #     username=USERNAME,
        #     password=PASSWORD,
        #     school=req.school,
        #     from_date=req.start_date,
        #     to_date=req.end_date,
        # )
        # print(f"✅ Fetch Teacher Notes : {time.time() - t:.2f} sec")
        # print("\n========== FETCHED TEACHER NOTES ==========")
        t = time.time()

        rows = service.get_teacher_notes(
            school=req.school,
            start_date=req.start_date,
            end_date=req.end_date
        )
        import json

        print("Rows fetched:", len(rows))

        if rows:
            print("\n===== FIRST RECORD =====")
            print(json.dumps(rows[0], indent=4))
            print("========================")
        print(f"Fetching notes took: {time.time() - t:.2f} sec")
        print("Rows fetched:", len(rows))

        # Print first record only once
        if rows:
            print("\n========== FIRST RECORD ==========")
            print(rows[0])
            print("Keys:", rows[0].keys())
            print("==================================")

        teacher_summary = {}
        print("\n===== 1. RAW API DATA =====") 
        for r in rows:

            # Safely get values (prevents KeyError)
            grade = str(r["grade"]).strip()
            teacher = str(r["username"]).strip()
            created_date = r["created_date"]

            print(f"Grade={grade}, Teacher={teacher}, Date={created_date}")

            key = (grade, teacher)

            if key not in teacher_summary:
                teacher_summary[key] = []

            teacher_summary[key].append(created_date)

        print("\n========== TEACHER SUMMARY ==========")
        for (grade, teacher), dates in sorted(teacher_summary.items()):
            print(
                f"Grade={grade:<5} "
                f"Teacher={teacher:<25} "
                f"Notes={len(dates)} "
                f"Dates={dates}"
            )

        print("\n===== ALL ROWS =====")
        print("\n===== 2. NORMALIZED DATA =====")
        for r in rows:
            print(
                repr(r.get("Username")),
                "| Grade:",
                repr(r.get("Grade")),
                "| Date:",
                r.get("Created_date")
            )

        print("====================")

        print("\n===== SPECIAL TEACHERS FOUND =====")
        for r in rows:
            if r.get("Username") in [
                "Vaishnavi",
                "Poonguzhali",
                "Kethsiyaal",
                "julian",
                "Gunavathi",
                "Sandhiya_saravanan",
                "Abinaya",
            ]:
                print(r)

        print("==================================")

        teacher_master = load_teacher_master()
        print("\n========== TEACHER MASTER ==========")

        for school, grades in teacher_master.items():
            print("\nSchool:", school)
            print("\n===== 3. FINAL GRADE MAP =====") 
            for grade, teachers in grades.items():
                print(f"{grade} -> {sorted(teachers)}")
                print("\n========== TEACHER MASTER ==========")
                print(teacher_master)
                print("====================================")

            print("Rows found:", len(rows))

        if not rows:
            print("No notes found. Showing all teachers from CSV.")
            rows = []

        
        # -------------------------------------------------------
        # Build Grade Map
        # -------------------------------------------------------
        t = time.time()
        grade_map = {}

        print("===== Grades from Database =====")
        print("\n===== ALL ROWS =====")

        for r in rows:

            grade = normalize_grade(r.get("grade"))

            teacher = (
                str(r.get("username", ""))
                .strip()
                .replace("  ", " ")
            )

            print(
                f"Teacher={teacher}, "
                f"Original Grade={repr(r.get('grade'))}, "
                f"Normalized Grade={grade}"
            )

            if grade not in grade_map:
                grade_map[grade] = {}

            if teacher not in grade_map[grade]:
                grade_map[grade][teacher] = []

            text = f"""
            Prepared:
            {r.get("what_i_prepared", "")}

            Did Well:
            {r.get("what_i_did_well", "")}

            Went Well:
            {r.get("what_went_well", "")}

            Needs Improvement:
            {r.get("where_to_improve", "")}

            Homework:
            {r.get("homework", "")}
            """

            if text not in grade_map[grade][teacher]:
                grade_map[grade][teacher].append(text)

        # ===========================
        # ADD THIS BLOCK HERE
        # ===========================
        print("\n========== GRADE MAP ==========")

        for grade, teachers in grade_map.items():
            print(f"\nGrade: {grade}")

            for teacher, notes in teachers.items():
                print(f"{teacher} -> {len(notes)} notes")

        print("================================")
        print(f"✅ Grade Map Creation : {time.time() - t:.2f} sec")
        # -------------------------------------------------------
        # Grade Order
        # -------------------------------------------------------
        grade_order = [
            "1st",
            "2nd",
            "3rd",
            "4th",
            "5th",
            "6th",
            "7th",
            "8th",
            "9th",
            "10th",
            "NIOS",
        ]

        print("Grade Order:", grade_order)
        print("Grade Map Keys:", list(grade_map.keys()))

        school_key = (
            req.school
            .strip()
            .lower()
            .replace(" ", "")
        )

        school_data = teacher_master.get(school_key, {})
        print("Requested School:", req.school)
        print("School Key:", school_key)
        print("Teacher Master Keys:", list(teacher_master.keys()))
        print("School Data:", school_data)
        print("\n===== EXPECTED 1st GRADE TEACHERS =====")
        print(school_data.get("1st", set()))

        print("School Key:", school_key)
        print("School Data:", school_data)
        print(teacher_master)
        special_teachers = school_data.get("Special", set())

        results = []

        # -------------------------------------------------------
        # Generate Grade-wise Feedback
        # -------------------------------------------------------
        for grade in grade_order:

            grade_result = {
                "grade": grade,
                "teachers": []
            }

            # Teachers expected from CSV
            expected_teachers = school_data.get(grade, set())

            # Teachers who submitted notes
            submitted_teachers = set(
                grade_map.get(grade, {}).keys()
            )

            # Merge both lists
            all_teachers = sorted(expected_teachers | submitted_teachers)

            print("----------------")
            print("Grade:", grade)
            print("Expected:", expected_teachers)
            print("Submitted:", submitted_teachers)
            print("All:", all_teachers)

            for teacher in all_teachers:

                # Teacher has submitted notes
                if teacher in grade_map.get(grade, {}):

                    entries = grade_map[grade][teacher]
                    notes_count = len(entries)

                    teacher_text = "\n\n----------------------\n\n".join(entries)

                    try:

                        print("\n" + "=" * 80)
                        print("STARTING FEEDBACK")
                        print("Teacher :", teacher)
                        print("Grade :", grade)
                        print("Notes Count :", notes_count)
                        print("Teacher Text Length :", len(teacher_text))
                        print("Teacher Text Words :", len(teacher_text.split()))
                        print("=" * 80)

                        # Start Timer
                        start_time = time.time()

                        feedback = generate_teacher_feedback(
                            grade,
                            teacher,
                            teacher_text,
                            notes_count
                        )

                        # End Timer
                        end_time = time.time()

                        print("\nReturned Feedback:")
                        print(repr(feedback))

                        print("\n" + "=" * 80)
                        print("FINISHED :", teacher)
                        print(
                            "Time Taken :",
                            round(end_time - start_time, 2),
                            "seconds"
                        )
                        print("=" * 80)

                    except Exception as e:

                        import traceback
                        traceback.print_exc()

                        feedback = f"Error generating feedback : {str(e)}"

                else:
                    # Teacher didn't submit notes
                    notes_count = 0
                    feedback = "Please fill the teacher notes."

                # Add teacher result
                grade_result["teachers"].append(
                    {
                        "teacher": teacher,
                        "notes_count": notes_count,
                        "feedback": feedback,
                    }
                )

            # Sort teachers alphabetically
            grade_result["teachers"].sort(
                key=lambda x: x["teacher"].lower()
            )

            # Add this grade
            results.append(grade_result)
        # ---------------------------------------
        # STEM / Computer / Art / Joyful English / Training
        # ---------------------------------------
        special_result = {
            "grade": "STEM Land / Computer Center / Art / Joyful English / Training",
            "teachers": []
        }

        for teacher in sorted(special_teachers):

            entries = []

            # Collect notes from every grade
            for grade_teachers in grade_map.values():
                if teacher in grade_teachers:
                    entries.extend(grade_teachers[teacher])

            if entries:

                notes_count = len(entries)

                teacher_text = "\n\n----------------------\n\n".join(entries)

                print("=" * 80)
                print("SPECIAL TEACHER:", teacher)
                print("NOTES:", notes_count)
                print("=" * 80)

                try:
                    start = time.time()
                    feedback = generate_teacher_feedback(
                        "Special",
                        teacher,
                        teacher_text,
                        notes_count
                    )
                    print(
                        f"Special Teacher {teacher} took {time.time() - start:.2f} sec"
                    )
                except Exception as e:
                    import traceback
                    traceback.print_exc()

                    feedback = f"Error generating feedback: {str(e)}"

            else:
                notes_count = 0
                feedback = "Please fill the teacher notes."

            special_result["teachers"].append({
                "teacher": teacher,
                "notes_count": notes_count,
                "feedback": feedback
            })

        special_result["teachers"].sort(
            key=lambda x: x["teacher"].lower()
        )

        results.append(special_result)

        # ---------------------------------------
        # DEBUG OUTPUT
        # ---------------------------------------
        print("\n========== FINAL RESULTS ==========")

        for group in results:
            print(f"\nGRADE: {group['grade']}")

            for teacher in group["teachers"]:
                print(
                    f"Teacher={teacher['teacher']}, "
                    f"Notes={teacher['notes_count']}"
                )

        print("===================================")
        
        return {
            "results": results
        }

    except Exception:
        import traceback

        error = traceback.format_exc()
        print(error)

        return {
            "error": error
        }