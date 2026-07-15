# backend/services/feedback_service.py

from backend.services.teacher_notes_service import TeacherNotesService
from backend.rag.query import generate_feedback


class FeedbackService:

    @classmethod
    def generate(cls, school_id, start_date, end_date):

        notes = TeacherNotesService.get_notes(
            school_id,
            start_date,
            end_date
        )

        return generate_feedback(notes["data"])