# test_teacher_notes_api.py

from backend.services.teacher_notes_service import (
    TeacherNotesService
)


service = TeacherNotesService()

data = service.get_teacher_notes(

        school="Udavi",
        start_date="2026-07-01",
        end_date="2026-07-06"

)

print(data)