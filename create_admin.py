from app import app
from extensions import db
from models import Admin
import os
import sys
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    db.create_all()
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not email or not password:
        print("[Erreur] ADMIN_EMAIL et ADMIN_PASSWORD doivent être définis dans .env")
        sys.exit(1)

    if len(password) < 8:
        print("[Erreur] ADMIN_PASSWORD doit contenir au moins 8 caractères.")
        sys.exit(1)

    if not Admin.query.filter_by(email=email).first():
        admin = Admin(email=email)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"[OK] Admin créé : {email}")
    else:
        print("[Info] Admin existe déjà.")