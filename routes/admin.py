from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import Admin, Project, Service, Skill, Experience, Hero, ContactInfo, Message
from extensions import db

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for("admin.dashboard"))
        flash("Identifiants invalides.", "error")
    return render_template("admin/login.html")

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))

@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "projects": Project.query.count(),
        "services": Service.query.count(),
        "skills": Skill.query.count(),
        "messages": Message.query.filter_by(status="unread").count(),
    }
    return render_template("admin/dashboard.html", stats=stats)