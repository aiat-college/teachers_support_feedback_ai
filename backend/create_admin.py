from backend.db.pgdatabase import SessionLocal
from backend.models.models import User
from backend.admin.security import hash_password

db = SessionLocal()

# Check if admin already exists
existing = db.query(User).filter(User.username == "admin").first()

if existing:
    print("Admin already exists")
else:
    admin_user = User(
        username="admin",
        email="admin@gmail.com",
        password_hash=hash_password("admin123"),
        full_name="Super Admin",
        phonenumber="9999999999",
        role="admin"
    )

    db.add(admin_user)
    db.commit()
    print("Admin created successfully")

db.close()