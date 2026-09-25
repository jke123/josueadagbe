from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from models import Hero, Project, Service, Skill, Experience, ContactInfo, Message
from extensions import db

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
    hero = Hero.query.first()
    projects = Project.query.order_by(Project.position).all()
    services = Service.query.order_by(Service.position).all()
    skills = Skill.query.order_by(Skill.category, Skill.position).all()
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    contact = ContactInfo.query.first()
    return render_template(
        "public/index.html",
        hero=hero, projects=projects, services=services,
        skills=skills, experiences=experiences, contact=contact,
    )

@public_bp.route("/contact", methods=["POST"])
def contact_submit():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    if not all([name, email, message]):
        flash("Merci de remplir les champs obligatoires.", "error")
        return redirect(url_for("public.index") + "#contact")

    msg = Message(name=name, email=email, subject=subject, message=message)
    db.session.add(msg)
    db.session.commit()
    flash("Message envoyé avec succès !", "success")
    return redirect(url_for("public.index") + "#contact")


@public_bp.route("/sitemap.xml")
def sitemap():
    pages = [url_for("public.index", _external=True)]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in pages:
        xml.append(f"<url><loc>{page}</loc></url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")
