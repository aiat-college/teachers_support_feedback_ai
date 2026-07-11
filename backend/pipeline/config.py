from pathlib import Path
from dotenv import load_dotenv
import os

# Project root folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env
env_path = BASE_DIR / ".env"

print("Loading .env from:", env_path)
print("Exists:", env_path.exists())

load_dotenv(dotenv_path=env_path)

# =====================================================
# WEBSITE CONFIGURATION
# =====================================================

BASE_URL = "https://teachersnotes.pythonanywhere.com"

LOGIN_URL = f"{BASE_URL}/accounts/login/"
SHOW_NOTES_URL = f"{BASE_URL}/ShowNotes"
HOME_URL = BASE_URL

# =====================================================
# LOGIN CREDENTIALS
# =====================================================

USERNAME = os.getenv("TEACHER_USERNAME")
PASSWORD = os.getenv("TEACHER_PASSWORD")

print("USERNAME =", repr(USERNAME))
print("PASSWORD =", repr(PASSWORD))

# =====================================================
# SCHOOL → GRADE MAPPING
# =====================================================

SCHOOL_GRADES = {
    "Udavi": [
        "4th", "5th", "6th", "7th", "8th", "9th", "10th"
    ],

    "Isaiambalam": [
        "1st", "2nd", "3rd", "4th", "5th",
        "6th", "7th", "8th", "NIOS"
    ],

    "Government School": [
        "Edayanchavady",
        "Bommarpalayam",
        "Kuyilappalayam"
    ],

    "AIAT": [
        "Hindi",
        "Applied Electronics & Chip Design year 1",
        "Applied Electronics & Chip Design year 2",
        "Green Energy & Electric System year 2",
        "Software Development year 1",
        "Software Development year 2",
        "Software Development year 3"
    ],

    "Aikiyam": [
        "9th",
        "10th"
    ],

    "NES": [
        "12th"
    ]
}