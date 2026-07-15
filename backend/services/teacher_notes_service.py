from backend.pipeline.scraper import fetch_teacher_notes
from backend.pipeline.config import USERNAME, PASSWORD
import traceback


class TeacherNotesService:

    def get_teacher_notes(
        self,
        school,
        start_date,
        end_date
    ):

        try:

            rows = fetch_teacher_notes(
                username=USERNAME,
                password=PASSWORD,
                school=school,
                from_date=start_date,
                to_date=end_date
            )

            return rows

        except Exception:

            print("\n===== ERROR IN TEACHER NOTES SERVICE =====")
            print(traceback.format_exc())
            print("==========================================")

            return []