from sqlalchemy import Column, Integer, String
from backend.db.pgdatabase import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    phonenumber = Column(String)
    photo_path = Column(String)
    role = Column(String, default="user")  # admin / user


class UserClass(Base):
    __tablename__ = "user_classes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    school = Column(String)
    grade = Column(String)
    

# ================= NOTE MODEL =================

class Note(Base):
    __tablename__ = "teacher_notes"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    school = Column(String)
    grade = Column(String)
    what_i_prepared = Column(String)
    what_i_did_well = Column(String)
    what_went_well = Column(String)
    where_to_improve = Column(String)
    created_date = Column(String)
    user_id = Column(Integer)
    what_homework_did_i_give = Column(String)