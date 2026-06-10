from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.admin.route import auth, users
from backend.routes import teacher_notes  # 👈 ADD THIS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Existing routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# 👇 NEW ROUTER FOR NOTES
app.include_router(teacher_notes.router, prefix="/notes", tags=["Teacher Notes"])