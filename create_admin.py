from app import app
from extensions import db
from models import Admin
import os
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    db.create_all()
    email = os.getenv("ADMIN_EMAIL")
    if not Admin.query.filter_by(email=email).first():
        admin = Admin(email=email)
        admin.set_password(os.getenv("ADMIN_PASSWORD"))
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Admin créé : {email}")
    else:
        print("ℹ️ Admin existe déjà.")