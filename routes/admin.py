from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from models import Admin, Project, Service, Skill, Experience, Hero, ContactInfo, Message
from extensions import db
from cloudinary_helper import upload_image
from datetime import datetime
import re

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")


def slugify(text):
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "projet"


def unique_slug(base_slug, exclude_id=None):
    """Garantit un slug unique en ajoutant -2, -3... si besoin."""
    slug = base_slug
    counter = 2
    query = Project.query.filter_by(slug=slug)
    if exclude_id:
        query = query.filter(Project.id != exclude_id)
    while query.first() is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1
        query = Project.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(Project.id != exclude_id)
    return slug


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ---------- AUTH ----------
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        admin = Admin.query.filter_by(email=email).first()

        if admin and admin.is_locked():
            flash("Compte temporairement verrouillé suite à plusieurs tentatives échouées. Réessaie dans 15 minutes.", "error")
            return render_template("admin/login.html")

        if admin and admin.check_password(password):
            admin.reset_attempts()
            db.session.commit()
            login_user(admin)
            return redirect(url_for("admin.dashboard"))

        if admin:
            admin.register_failed_attempt()
            db.session.commit()

        flash("Identifiants invalides.", "error")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


# ---------- DASHBOARD ----------
@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "projects": Project.query.count(),
        "services": Service.query.count(),
        "skills": Skill.query.count(),
        "experiences": Experience.query.count(),
        "messages": Message.query.filter_by(status="unread").count(),
    }
    return render_template("admin/dashboard.html", stats=stats)


# ---------- HERO ----------
@admin_bp.route("/hero", methods=["GET", "POST"])
@login_required
def hero_edit():
    hero = Hero.query.first()
    if not hero:
        hero = Hero(title="Bienvenue")
        db.session.add(hero)
        db.session.commit()

    if request.method == "POST":
        hero.title = request.form.get("title")
        hero.subtitle = request.form.get("subtitle")
        hero.description = request.form.get("description")

        file = request.files.get("background_image")
        if file and file.filename:
            url = upload_image(file, folder="portfolio/hero")
            if url:
                hero.background_image = url

        db.session.commit()
        flash("Hero mis à jour.", "success")
        return redirect(url_for("admin.hero_edit"))

    return render_template("admin/hero.html", hero=hero)


# ---------- PROJECTS ----------
@admin_bp.route("/projects")
@login_required
def projects_list():
    projects = Project.query.order_by(Project.position).all()
    return render_template("admin/projects.html", projects=projects)


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def project_new():
    if request.method == "POST":
        file = request.files.get("image")
        image_url = upload_image(file, folder="portfolio/projects") if file and file.filename else None

        tech_raw = request.form.get("technologies", "")
        tech_list = [t.strip() for t in tech_raw.split(",") if t.strip()]

        title = request.form.get("title", "")
        raw_slug = request.form.get("slug") or title
        slug = unique_slug(slugify(raw_slug))

        project = Project(
            title=title,
            slug=slug,
            description=request.form.get("description"),
            image_url=image_url,
            demo_url=request.form.get("demo_url"),
            code_url=request.form.get("code_url"),
            technologies=tech_list,
            featured=bool(request.form.get("featured")),
            position=safe_int(request.form.get("position"), 0),
        )
        try:
            db.session.add(project)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Impossible de créer ce projet (conflit de données). Réessaie.", "error")
            return render_template("admin/project_form.html", project=None)

        flash("Projet créé.", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template("admin/project_form.html", project=None)


@admin_bp.route("/projects/<int:id>/edit", methods=["GET", "POST"])
@login_required
def project_edit(id):
    project = Project.query.get_or_404(id)

    if request.method == "POST":
        project.title = request.form.get("title")
        raw_slug = request.form.get("slug") or project.title
        project.slug = unique_slug(slugify(raw_slug), exclude_id=project.id)
        project.description = request.form.get("description")
        project.demo_url = request.form.get("demo_url")
        project.code_url = request.form.get("code_url")
        project.featured = bool(request.form.get("featured"))
        project.position = safe_int(request.form.get("position"), 0)

        tech_raw = request.form.get("technologies", "")
        project.technologies = [t.strip() for t in tech_raw.split(",") if t.strip()]

        file = request.files.get("image")
        if file and file.filename:
            url = upload_image(file, folder="portfolio/projects")
            if url:
                project.image_url = url

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Impossible de mettre à jour ce projet (conflit de données). Réessaie.", "error")
            return render_template("admin/project_form.html", project=project)

        flash("Projet mis à jour.", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template("admin/project_form.html", project=project)


@admin_bp.route("/projects/<int:id>/delete", methods=["POST"])
@login_required
def project_delete(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Projet supprimé.", "success")
    return redirect(url_for("admin.projects_list"))


# ---------- SERVICES ----------
@admin_bp.route("/services")
@login_required
def services_list():
    services = Service.query.order_by(Service.position).all()
    return render_template("admin/services.html", services=services)


@admin_bp.route("/services/new", methods=["GET", "POST"])
@login_required
def service_new():
    if request.method == "POST":
        service = Service(
            title=request.form.get("title"),
            description=request.form.get("description"),
            icon=request.form.get("icon"),
            position=safe_int(request.form.get("position"), 0),
        )
        db.session.add(service)
        db.session.commit()
        flash("Service créé.", "success")
        return redirect(url_for("admin.services_list"))
    return render_template("admin/service_form.html", service=None)


@admin_bp.route("/services/<int:id>/edit", methods=["GET", "POST"])
@login_required
def service_edit(id):
    service = Service.query.get_or_404(id)
    if request.method == "POST":
        service.title = request.form.get("title")
        service.description = request.form.get("description")
        service.icon = request.form.get("icon")
        service.position = safe_int(request.form.get("position"), 0)
        db.session.commit()
        flash("Service mis à jour.", "success")
        return redirect(url_for("admin.services_list"))
    return render_template("admin/service_form.html", service=service)


@admin_bp.route("/services/<int:id>/delete", methods=["POST"])
@login_required
def service_delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash("Service supprimé.", "success")
    return redirect(url_for("admin.services_list"))


# ---------- SKILLS ----------
@admin_bp.route("/skills")
@login_required
def skills_list():
    skills = Skill.query.order_by(Skill.category, Skill.position).all()
    return render_template("admin/skills.html", skills=skills)


@admin_bp.route("/skills/new", methods=["GET", "POST"])
@login_required
def skill_new():
    if request.method == "POST":
        skill = Skill(
            name=request.form.get("name"),
            level=safe_int(request.form.get("level"), 0),
            category=request.form.get("category"),
            position=safe_int(request.form.get("position"), 0),
        )
        db.session.add(skill)
        db.session.commit()
        flash("Compétence créée.", "success")
        return redirect(url_for("admin.skills_list"))
    return render_template("admin/skill_form.html", skill=None)


@admin_bp.route("/skills/<int:id>/edit", methods=["GET", "POST"])
@login_required
def skill_edit(id):
    skill = Skill.query.get_or_404(id)
    if request.method == "POST":
        skill.name = request.form.get("name")
        skill.level = safe_int(request.form.get("level"), 0)
        skill.category = request.form.get("category")
        skill.position = safe_int(request.form.get("position"), 0)
        db.session.commit()
        flash("Compétence mise à jour.", "success")
        return redirect(url_for("admin.skills_list"))
    return render_template("admin/skill_form.html", skill=skill)


@admin_bp.route("/skills/<int:id>/delete", methods=["POST"])
@login_required
def skill_delete(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash("Compétence supprimée.", "success")
    return redirect(url_for("admin.skills_list"))


# ---------- EXPERIENCES ----------
@admin_bp.route("/experiences")
@login_required
def experiences_list():
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    return render_template("admin/experiences.html", experiences=experiences)


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date() if value else None
    except ValueError:
        return None


@admin_bp.route("/experiences/new", methods=["GET", "POST"])
@login_required
def experience_new():
    if request.method == "POST":
        exp = Experience(
            title=request.form.get("title"),
            company=request.form.get("company"),
            location=request.form.get("location"),
            start_date=parse_date(request.form.get("start_date")),
            end_date=parse_date(request.form.get("end_date")),
            is_current=bool(request.form.get("is_current")),
            description=request.form.get("description"),
            position=safe_int(request.form.get("position"), 0),
        )
        db.session.add(exp)
        db.session.commit()
        flash("Expérience créée.", "success")
        return redirect(url_for("admin.experiences_list"))
    return render_template("admin/experience_form.html", experience=None)


@admin_bp.route("/experiences/<int:id>/edit", methods=["GET", "POST"])
@login_required
def experience_edit(id):
    exp = Experience.query.get_or_404(id)
    if request.method == "POST":
        exp.title = request.form.get("title")
        exp.company = request.form.get("company")
        exp.location = request.form.get("location")
        exp.start_date = parse_date(request.form.get("start_date"))
        exp.end_date = parse_date(request.form.get("end_date"))
        exp.is_current = bool(request.form.get("is_current"))
        exp.description = request.form.get("description")
        exp.position = safe_int(request.form.get("position"), 0)
        db.session.commit()
        flash("Expérience mise à jour.", "success")
        return redirect(url_for("admin.experiences_list"))
    return render_template("admin/experience_form.html", experience=exp)


@admin_bp.route("/experiences/<int:id>/delete", methods=["POST"])
@login_required
def experience_delete(id):
    exp = Experience.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    flash("Expérience supprimée.", "success")
    return redirect(url_for("admin.experiences_list"))


# ---------- CONTACT INFO ----------
@admin_bp.route("/contact", methods=["GET", "POST"])
@login_required
def contact_edit():
    contact = ContactInfo.query.first()
    if not contact:
        contact = ContactInfo()
        db.session.add(contact)
        db.session.commit()

    if request.method == "POST":
        contact.email = request.form.get("email")
        contact.phone = request.form.get("phone")
        contact.address = request.form.get("address")
        contact.linkedin = request.form.get("linkedin")
        contact.github = request.form.get("github")
        contact.twitter = request.form.get("twitter")
        db.session.commit()
        flash("Coordonnées mises à jour.", "success")
        return redirect(url_for("admin.contact_edit"))

    return render_template("admin/contact.html", contact=contact)


# ---------- MESSAGES ----------
@admin_bp.route("/messages")
@login_required
def messages_list():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("admin/messages.html", messages=messages)


@admin_bp.route("/messages/<int:id>/read", methods=["POST"])
@login_required
def message_mark_read(id):
    msg = Message.query.get_or_404(id)
    msg.status = "read"
    db.session.commit()
    return redirect(url_for("admin.messages_list"))


@admin_bp.route("/messages/<int:id>/delete", methods=["POST"])
@login_required
def message_delete(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message supprimé.", "success")
    return redirect(url_for("admin.messages_list"))