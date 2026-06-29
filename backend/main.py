from fastapi.responses import FileResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from backend.admin.route import auth, users
from backend.db.pgdatabase import Base,engine,SessionLocal
from backend.models.models import User,Note as NoteModel, UserClass
from backend.admin.security import verify_password, create_access_token,SECRET_KEY,ALGORITHM
from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime, timedelta
from jose import jwt, JWTError
import psycopg2
import os
app = FastAPI()
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "database.sqlite3"

def get_db_connection():
    print("DB FILE:", DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def fetch_teacher_entries(school, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Debug: show available tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)
    print("Tables:", [row[0] for row in cursor.fetchall()])

    query = """
    SELECT
        Username,
        School,
        Grade,
        What_I_prepared,
        What_I_did_well,
        What_went_well,
        Where_to_improve,
        Created_date,
        What_homework_did_I_give_today
    FROM Notes_notes
    WHERE School = ?
    AND Created_date BETWEEN ? AND ?
    """

    cursor.execute(
        query,
        (school, start_date, end_date)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
# ================= APP ===================

app = FastAPI()
Base.metadata.create_all(bind=engine)
# ================= CORS ==================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ================= FRONTEND PATH =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_PATH = os.path.join(BASE_DIR, "../frontend/dist")
# ================= SERVE FRONTEND =================

Base.metadata.create_all(bind=engine)

# Serve assets
if os.path.exists(FRONTEND_PATH):

    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(FRONTEND_PATH, "assets")),
        name="assets"
    )

# Main React page
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))

# ================= DATABASE =================

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="TeacherNotes",
        user="postgres",
        password="aiat"
    )


# Backwards-compatible alias: preserve old /login path used by some frontend builds
@app.post("/login")
async def login_alias():
    return RedirectResponse(url="/user-login", status_code=307)

# ================= AUTH =================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class NoteCreate(BaseModel):
    school: str
    grade: str
    what_i_prepared: str
    what_i_did_well: str
    what_went_well: str
    where_to_improve: str
    created_date: str
    what_homework_did_i_give: str

class NoteResponse(BaseModel):
    id: int
    username: str
    school: str
    grade: str
    what_i_prepared: str
    what_i_did_well: str
    what_went_well: str
    where_to_improve: str
    created_date: str
    what_homework_did_i_give: str

    class Config:
        from_attributes = True  # IMPORTANT for SQLAlchemy



class LoginRequest(BaseModel):
    username: str
    password: str


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
#================== AUTH  =================

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# ================= LOGIN =================
@app.post("/user-login")
def user_login(data: LoginRequest):

    
    db = SessionLocal()
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.role != "user":
        raise HTTPException(status_code=403, detail="Not an admin")

    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token}




@app.get("/dashboard")
def dashboard(user: dict = Depends(get_current_user)):

    db = SessionLocal()

    username = user["sub"]

    db_user = db.query(User).filter(
        User.username == username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    classes = db.query(UserClass).filter(
        UserClass.user_id == db_user.id
    ).all()

    return {
        "username": db_user.full_name,
        "profile_image": db_user.photo_path,
        "classes": []
    }
# ================= SAVE =================

@app.post("/write")
def save_note(note: NoteCreate, user: dict = Depends(get_current_user)):

    db = SessionLocal()

    username = user["sub"]

    db_user = db.query(User).filter(
        User.username == username
    ).first()
    new_note = NoteModel(
        username=username,
        user_id=db_user.id,
        school=note.school,
        grade=note.grade,
        what_i_prepared=note.what_i_prepared,
        what_i_did_well=note.what_i_did_well,
        what_went_well=note.what_went_well,
        where_to_improve=note.where_to_improve,
        created_date=note.created_date,
        what_homework_did_i_give=note.what_homework_did_i_give
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {"message": "Saved Successfully"}


# ================= GET ALL =================

@app.get("/notes", response_model=list[NoteResponse])
def get_all_notes(user: dict = Depends(get_current_user)):

    db = SessionLocal()

    notes = (
        db.query(NoteModel)
        .order_by(NoteModel.created_date.desc())
        .all()
    )

    return notes

# ================= DATE FILTER =================

#def get_notes_by_date(
    #from_date: str,
    #to_date: str,
    #user: dict = Depends(get_current_user)
#):


# ================= GET ONE =================
@app.get("/notes/{id}", response_model=NoteResponse)
def get_note(id: int, user: str = Depends(get_current_user)):

    db = SessionLocal()

    db_note = db.query(NoteModel).filter(NoteModel.id == id).first()

    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    
    return db_note


# ================= UPDATE (7 DAYS LIMIT) =================
@app.put("/notes/{id}")
def update_note(id: int, note: NoteCreate, user: str = Depends(get_current_user)):

    db = SessionLocal()

    db_note = db.query(NoteModel).filter(NoteModel.id == id).first()

    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    created = datetime.strptime(str(db_note.created_date), "%Y-%m-%d")

    if datetime.now() - created > timedelta(days=7):
        raise HTTPException(status_code=400, detail="Edit expired (7 days limit)")

    db_note.school = note.school
    db_note.grade = note.grade
    db_note.what_i_prepared = note.what_i_prepared
    db_note.what_i_did_well = note.what_i_did_well
    db_note.what_went_well = note.what_went_well
    db_note.where_to_improve = note.where_to_improve
    db_note.created_date = note.created_date
    db_note.what_homework_did_i_give = note.what_homework_did_i_give

    db.commit()
    db.refresh(db_note)

    return {"message": "Updated successfully"}


# ================= DELETE =================

@app.delete("/notes/{id}")
def delete_note(id: int, user: str = Depends(get_current_user)):

    db = SessionLocal()

    note = db.query(NoteModel).filter(NoteModel.id == id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(note)
    db.commit()

    return {"message": "Deleted"}

@app.get("/")
def serve_frontend():

    index_file = os.path.join(
        FRONTEND_PATH,
        "index.html"
    )

    if os.path.exists(index_file):
        return FileResponse(index_file)

    return {"message": "Frontend not built"}
# ================= REACT ROUTER FIX =================
# IMPORTANT: Keep this at bottom

# @app.get("/{full_path:path}")
# def serve_react_app(full_path: str):

#     index_file = os.path.join(FRONTEND_PATH, "index.html")

#     if os.path.exists(index_file):
#         return FileResponse(index_file)

#     return {"error": "Frontend not built"}
