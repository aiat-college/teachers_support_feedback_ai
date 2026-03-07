from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.admin.route import auth, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],                      # <-- VERY IMPORTANT
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])