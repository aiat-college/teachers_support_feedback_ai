import os

def save_teacher_output(teacher, content):
    folder = "outputs/teachers"
    os.makedirs(folder, exist_ok=True)

    filename = f"{folder}/{teacher}_suggestions.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
