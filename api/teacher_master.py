from pathlib import Path
import pandas as pd


def load_teacher_master():
    """
    Load teacher mapping from teacher_grades_match.csv

    Returns:
    {
        "schoolname": {
            "1st": {"Teacher1", "Teacher2"},
            "2nd": {...},
            ...
            "Special": {...}
        }
    }
    """

    BASE_DIR = Path(__file__).resolve().parent.parent

    csv_file = BASE_DIR / "data" / "teacher_grades_match.csv"

    print("Loading Teacher Master...")
    print("CSV Path:", csv_file)

    if not csv_file.exists():
        raise FileNotFoundError(f"{csv_file} not found")

    df = pd.read_csv(csv_file)

    print(df[["School", "Grade", "Username"]])

    teacher_master = {}

    for _, row in df.iterrows():

        school = str(row["School"]).strip().lower().replace(" ", "")

        grade = str(row["Grade"]).strip().lower()

        teacher = str(row["Username"]).strip()

        # Normalize grade
        grade_map = {
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
        "nios": "NIOS",
        "special": "Special",
        "all": "Special"
    }

        grade = grade_map.get(grade, grade)

        if school not in teacher_master:
            teacher_master[school] = {}

        if grade not in teacher_master[school]:
            teacher_master[school][grade] = set()

        teacher_master[school][grade].add(teacher)

    print("\n===== LOADED TEACHER MASTER =====")

    for school, grades in teacher_master.items():
        print("\nSchool:", school)

        for grade, teachers in grades.items():
            print(
                f"{grade:<8} -> {sorted(teachers)}"
            )

    print("===============================")

    return teacher_master