from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .auth import admin_required, authenticate_admin
from .extensions import db
from .models import ContactMessage
from .services import (
    KOSOVO_CITIES,
    SERVICE_CATEGORIES,
    clear_home_banner,
    create_freelancer_from_form,
    delete_freelancer as remove_freelancer,
    delete_message as remove_message,
    get_freelancer_by_id,
    get_freelancers,
    get_home_banner,
    get_messages,
    save_freelancer,
    save_home_banner_upload,
    validate_freelancer_form,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def render_admin(section, freelancer=None):
    return render_template(
        "admin.html",
        section=section,
        freelancer=freelancer,
        freelancers=get_freelancers(),
        messages=get_messages(),
        categories=SERVICE_CATEGORIES,
        cities=KOSOVO_CITIES,
        banner=get_home_banner(),
    )


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if authenticate_admin(username, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        flash("Username ose password i gabuar.", "error")
    return render_template("admin-login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@admin_bp.route("")
@admin_bp.route("/")
@admin_required
def dashboard():
    return render_admin("dashboard")


@admin_bp.route("/freelancers")
@admin_required
def list_freelancers():
    return render_admin("list")


@admin_bp.route("/freelancers/add", methods=["GET", "POST"])
@admin_required
def add_freelancer():
    if request.method == "POST":
        if not validate_freelancer_form(request.form):
            flash("Plotësoni të gjitha fushat e detyrueshme për freelancerin.", "error")
            return render_admin("form")
        freelancer = create_freelancer_from_form(request.form, request.files.get("image_upload"))
        save_freelancer(freelancer)
        flash("Freelanceri u shtua me sukses.", "success")
        return redirect(url_for("admin.list_freelancers"))
    return render_admin("form")


@admin_bp.route("/freelancers/edit/<int:freelancer_id>", methods=["GET", "POST"])
@admin_required
def edit_freelancer(freelancer_id):
    freelancer = get_freelancer_by_id(freelancer_id)
    if freelancer is None:
        flash("Freelanceri nuk u gjet.", "error")
        return redirect(url_for("admin.list_freelancers"))

    if request.method == "POST":
        if not validate_freelancer_form(request.form):
            flash("Plotësoni të gjitha fushat e detyrueshme për freelancerin.", "error")
            return render_admin("form", freelancer=freelancer)
        create_freelancer_from_form(request.form, request.files.get("image_upload"), existing=freelancer)
        save_freelancer(freelancer)
        flash("Ndryshimet u ruajtën me sukses.", "success")
        return redirect(url_for("admin.list_freelancers"))

    return render_admin("form", freelancer=freelancer)


@admin_bp.route("/freelancers/delete/<int:freelancer_id>", methods=["POST"])
@admin_required
def delete_freelancer(freelancer_id):
    freelancer = get_freelancer_by_id(freelancer_id)
    if freelancer is None:
        flash("Freelanceri nuk u gjet.", "error")
    else:
        remove_freelancer(freelancer)
        flash("Freelanceri u fshi.", "success")
    return redirect(url_for("admin.list_freelancers"))


@admin_bp.route("/messages")
@admin_required
def messages():
    return render_admin("messages")


@admin_bp.route("/banner", methods=["GET", "POST"])
@admin_required
def banner():
    if request.method == "POST":
        uploaded_image = save_home_banner_upload(request.files.get("image_upload"))
        if uploaded_image:
            flash("Banneri u ruajt me sukses.", "success")
        else:
            flash("Zgjidhni një foto valide për bannerin.", "error")
        return redirect(url_for("admin.banner"))
    return render_admin("banner")


@admin_bp.route("/banner/delete", methods=["POST"])
@admin_required
def delete_banner():
    clear_home_banner()
    flash("Fotoja e bannerit u fshi.", "success")
    return redirect(url_for("admin.banner"))


@admin_bp.route("/messages/delete/<int:message_id>", methods=["POST"])
@admin_required
def delete_message(message_id):
    message = db.session.get(ContactMessage, message_id)
    if message is None:
        flash("Mesazhi nuk u gjet.", "error")
    else:
        remove_message(message)
        flash("Mesazhi u fshi.", "success")
    return redirect(url_for("admin.messages"))
