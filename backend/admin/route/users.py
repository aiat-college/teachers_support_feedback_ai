from fastapi import APIRouter, Depends, UploadFile, File, Form
from backend.models.models import User
from backend.db.pgdatabase import SessionLocal
from backend.admin.security import hash_password
from backend.admin.dependency import admin_required
import shutil, os

router = APIRouter()

@router.post("/create", dependencies=[Depends(admin_required)])
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    phonenumber: str = Form(...),
    school: str = Form(...),
    grade: str = Form(...),
    photo: UploadFile = File(None)
):
    db = SessionLocal()

    photo_path = None
    if photo:
        os.makedirs("uploads", exist_ok=True)
        photo_path = f"uploads/{photo.filename}"
        with open(photo_path, "wb") as f:
            shutil.copyfileobj(photo.file, f)

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        phonenumber = phonenumber,
        photo_path=photo_path,
        school=school,
        grade=grade,
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}
