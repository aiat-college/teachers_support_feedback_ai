from fastapi import APIRouter, Depends, UploadFile, File, Form
from backend.models.models import User, UserClass
from backend.db.pgdatabase import SessionLocal
from backend.admin.security import hash_password
from backend.admin.dependency import admin_required
import shutil, os
import json

router = APIRouter()

@router.post("/create", dependencies=[Depends(admin_required)])
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    phonenumber: str = Form(...),
    classes: str = Form(...),
    photo: UploadFile = File(None)
):
    
    classes = json.loads(classes)
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
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    for c in classes:
        user_class = UserClass(
            user_id=user.id,
            school=c["school"],
            grade=c["grade"]
        )

        db.add(user_class)

    db.commit()

    return {"message": "User created successfully"}
