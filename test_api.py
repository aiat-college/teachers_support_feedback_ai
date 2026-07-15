from backend.services.teacher_notes_api import TeacherNotesAPI

api = TeacherNotesAPI()

try:
    data = api.get_teacher_notes(
        school="Udavi",
        start_date="2026-07-01",
        end_date="2026-07-07",
    )

    print("\n===== SUCCESS =====")
    print(type(data))
    print(data)

except Exception as e:
    print("\n===== FAILED =====")
    print(e)