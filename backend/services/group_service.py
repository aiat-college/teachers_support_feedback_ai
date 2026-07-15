from collections import defaultdict

def group_by_teacher(rows):

    teachers = defaultdict(list)

    for row in rows:

        teacher = row[0]

        note = f"""
Prepared: {row[1]}
Did Well: {row[2]}
Went Well: {row[3]}
Improve: {row[4]}
Homework: {row[5]}
Date: {row[6]}
"""

        teachers[teacher].append(note)

    return teachers