# backend/services/teacher_notes_api.py

import requests
import traceback

from backend.pipeline.config import (
    API_BASE_URL,
    TEACHER_NOTES_ENDPOINT,
    API_TIMEOUT,
)

class TeacherNotesAPI:
    """
    Handles all Teacher Notes REST API operations.

    NOTE:
    -----
    The actual API has not been deployed yet.
    This class is prepared for future integration.

    Once the website owner deploys the API,
    only this file needs to be updated.
    """

    def __init__(self):

        self.base_url = API_BASE_URL
        self.endpoint = TEACHER_NOTES_ENDPOINT
        self.timeout = API_TIMEOUT

    def get_teacher_notes(
        self,
        school,
        start_date,
        end_date,
    ):
        """
        Fetch teacher notes from the REST API.

        Parameters
        ----------
        school : str
            School name.

        start_date : str
            Start date (YYYY-MM-DD).

        end_date : str
            End date (YYYY-MM-DD).


        Returns
        -------
        list
            Returns teacher notes.

        Raises
        ------
        NotImplementedError
            If the API is not available.
        """

        # ------------------------------------
        # API NOT AVAILABLE YET
        # ------------------------------------

        if not self.base_url:

            raise NotImplementedError(

                "Teacher Notes API is not available yet."
                "\nWaiting for API deployment."

            )

        # ------------------------------------
        # FUTURE IMPLEMENTATION
        # ------------------------------------

        try:

            url = f"{self.base_url}{self.endpoint}"

            response = requests.get(

                url,

                params={

                    "school": school,
                    "startDate": start_date,
                    "endDate": end_date,

                },

                timeout=self.timeout,

            )

            response.raise_for_status()

            result = response.json()

            if result.get("success"):

                return result.get("data", [])

            return []

        except requests.exceptions.Timeout:

            print("\n===== API TIMEOUT ERROR =====")
            print("Teacher Notes API timed out.")
            print("============================\n")

            return []

        except requests.exceptions.ConnectionError:

            print("\n===== CONNECTION ERROR =====")
            print("Unable to connect to API.")
            print("============================\n")

            return []

        except requests.exceptions.HTTPError as e:

            print("\n===== HTTP ERROR =====")
            print(e)
            print("======================\n")

            return []

        except Exception:

            print("\n===== API ERROR =====")
            print(traceback.format_exc())
            print("=====================\n")

            return []