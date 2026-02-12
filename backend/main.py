from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
import psycopg2
import os
# ================= CONFIG =================

SECRET_KEY = "be2a1efff37b0737fb6143f1935d0ac30cc1bc49517259e6540f500ba4751304"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ================= APP ===================

app = FastAPI()
# ================= CORS ======================

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

# ================= AUTH =================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


fake_users_db = {
    "teacher": {"username": "teacher", "password": "1234"}
}


class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

# ================= LOGIN =================

@app.post("/login")
def login(data: LoginRequest):

    user = fake_users_db.get(data.username)

    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user["username"]
    }


@app.get("/dashboard")
def dashboard(user: str = Depends(get_current_user)):

    return {"message": f"Welcome {user}"}

 
# ================= NOTE MODEL =================

class Note(BaseModel):

    username: str
    school: str
    grade: str
    what_i_prepared: str
    what_i_did_well: str
    what_went_well: str
    where_to_improve: str
    created_date: str
    user_id: int
    what_homework_did_i_give: str


# ================= SAVE =================

@app.post("/save")
def save_note(note: Note):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO teacher_notes (
            username,
            school,
            grade,
            what_i_prepared,
            what_i_did_well,
            what_went_well,
            where_to_improve,
            created_date,
            user_id,
            what_homework_did_i_give
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        note.username,
        note.school,
        note.grade,
        note.what_i_prepared,
        note.what_i_did_well,
        note.what_went_well,
        note.where_to_improve,
        note.created_date,
        note.user_id,
        note.what_homework_did_i_give
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Saved Successfully"}


# ================= GET ALL =================

@app.get("/notes")
def get_all_notes():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM teacher_notes
        ORDER BY created_date DESC, id DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for r in rows:

        result.append({
            "id": r[0],
            "username": r[1],
            "school": r[2],
            "grade": r[3],
            "what_i_prepared": r[4],
            "what_i_did_well": r[5],
            "what_went_well": r[6],
            "where_to_improve": r[7],
            "created_date": str(r[8]),
            "user_id": r[9],
            "what_homework_did_i_give": r[10]
        })

    return result


# ================= DATE FILTER =================

@app.get("/notes-by-date")
def get_notes_by_date(from_date: str, to_date: str):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM teacher_notes
        WHERE created_date BETWEEN %s AND %s
        ORDER BY created_date DESC
    """, (from_date, to_date))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for r in rows:

        result.append({
            "id": r[0],
            "username": r[1],
            "school": r[2],
            "grade": r[3],
            "what_i_prepared": r[4],
            "what_i_did_well": r[5],
            "what_went_well": r[6],
            "where_to_improve": r[7],
            "created_date": str(r[8]),
            "user_id": r[9],
            "what_homework_did_i_give": r[10]
        })

    return result


# ================= GET ONE =================

@app.get("/notes/{id}")
def get_note(id: int):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM teacher_notes WHERE id=%s", (id,))

    r = cur.fetchone()

    cur.close()
    conn.close()

    if not r:
        return {"error": "Not found"}

    return {
        "id": r[0],
        "username": r[1],
        "school": r[2],
        "grade": r[3],
        "what_i_prepared": r[4],
        "what_i_did_well": r[5],
        "what_went_well": r[6],
        "where_to_improve": r[7],
        "created_date": str(r[8]),
        "user_id": r[9],
        "what_homework_did_i_give": r[10]
    }


# ================= UPDATE (7 DAYS LIMIT) =================

@app.put("/notes/{id}")
def update_note(id: int, note: Note):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT created_date FROM teacher_notes WHERE id=%s", (id,)
    )

    row = cur.fetchone()

    if not row:
        return {"error": "Not found"}

    created = datetime.strptime(str(row[0]), "%Y-%m-%d")

    if datetime.now() - created > timedelta(days=7):
        return {"error": "Edit expired (7 days limit)"}

    cur.execute("""
        UPDATE teacher_notes
        SET
            username=%s,
            school=%s,
            grade=%s,
            what_i_prepared=%s,
            what_i_did_well=%s,
            what_went_well=%s,
            where_to_improve=%s,
            created_date=%s,
            user_id=%s,
            what_homework_did_i_give=%s
        WHERE id=%s
    """, (
        note.username,
        note.school,
        note.grade,
        note.what_i_prepared,
        note.what_i_did_well,
        note.what_went_well,
        note.where_to_improve,
        note.created_date,
        note.user_id,
        note.what_homework_did_i_give,
        id
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Updated"}


# ================= DELETE =================

@app.delete("/notes/{id}")
def delete_note(id: int):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM teacher_notes WHERE id=%s", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Deleted"}


# ================= REACT ROUTER FIX =================
# IMPORTANT: Keep this at bottom

@app.get("/{full_path:path}")
def serve_react_app(full_path: str):

    index_file = os.path.join(FRONTEND_PATH, "index.html")

    if os.path.exists(index_file):
        return FileResponse(index_file)

    return {"error": "Frontend not built"}
