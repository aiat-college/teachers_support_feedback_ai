from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.admin.route import auth, users
from backend.db.pgdatabase import Base,engine,SessionLocal
from backend.models.models import User,Note as NoteModel
from backend.admin.security import verify_password, create_access_token
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
    
#================== AUTH  =================

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# ================= LOGIN =================

@app.post("/login")
def login(data: LoginRequest):

    db = SessionLocal()
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.role != "user":
        raise HTTPException(status_code=403, detail="Not an admin")

    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token}


@app.get("/dashboard")
def dashboard(user: str = Depends(get_current_user)):

    db = SessionLocal()

    db_user = db.query(User).filter(User.username == user).first()


    return {
        "username": db_user.full_name,
        "profile_image": db_user.photo_path   # stored image path
    }

# ================= SAVE =================

@app.post("/write")
def save_note(note: NoteCreate, user: str = Depends(get_current_user)):

    db = SessionLocal()

    db_user = db.query(User).filter(User.username == user).first()

    new_note = NoteModel(
        username=user,
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
def get_all_notes(user: str = Depends(get_current_user)):

    db = SessionLocal()
    notes = db.query(NoteModel).order_by(NoteModel.created_date.desc()).all()
    return notes


# ================= DATE FILTER =================

@app.get("/notes-by-date", response_model=list[NoteResponse])
def get_notes_by_date(from_date: str, to_date: str,user: str = Depends(get_current_user)):

    db = SessionLocal()

    db_user = db.query(User).filter(User.username == user).first()

    notes = db.query(NoteModel).filter(
        NoteModel.created_date.between(from_date, to_date)
    ).order_by(NoteModel.created_date.desc()).all()

    return notes


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


# ================= REACT ROUTER FIX =================
# IMPORTANT: Keep this at bottom

@app.get("/{full_path:path}")
def serve_react_app(full_path: str):

    index_file = os.path.join(FRONTEND_PATH, "index.html")

    if os.path.exists(index_file):
        return FileResponse(index_file)

    return {"error": "Frontend not built"}
