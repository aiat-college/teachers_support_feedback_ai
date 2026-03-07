from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TeacherNotes(Base):
    __tablename__ = "teacher_notes"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, index=True, nullable=False)

    date = Column(Date, nullable=False)
    subject = Column(String(100), nullable=False)
    class_name = Column(String(50), nullable=False)

    routine_notes = Column(Text, nullable=False)
    feedback = Column(Text, nullable=True)
