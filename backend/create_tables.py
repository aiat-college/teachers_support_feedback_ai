# import sys
# import os

# from backend.db.pgdatabase import engine
# from backend.models.models import User

# User.metadata.create_all(bind=engine)

# print("Tables created successfully")

from backend.db.pgdatabase import engine
from backend.models.models import Base  # import Base
from backend.models.models import User
from backend.models.teacher_notes import TeacherNotes  # make sure this exists

# Create all tables
Base.metadata.create_all(bind=engine)

print("All tables created successfully")