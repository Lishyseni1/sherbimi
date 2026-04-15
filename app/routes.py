from flask import Blueprint, abort, flash, redirect, render_template, request, send_file, url_for
from io import BytesIO

from .models import UploadedImage
from .services import (
    KOSOVO_CITIES,
    SERVICE_CATEGORIES,
    create_message,
    get_freelancer_by_id,
    get_freelancers,
    get_home_banner,
    merge_options,
    validate_contact_form,
)

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
@public_bp.route("/index.html")
def index():
    freelancers = get_freelancers()
    premium = [item for item in freelancers if item.premium][:3]
    return render_template("index.html", freelancers=premium, home_banner=get_home_banner())


@public_bp.route("/freelancers")
@public_bp.route("/freelancers.html")
def freelancers():
    all_freelancers = get_freelancers()
    search = request.args.get("search", "").lower().strip()
    category = request.args.get("category", "").strip()
    city = request.args.get("city", "").strip()

    filtered = []
    for freelancer in all_freelancers:
        text = " ".join(
            [
                freelancer.name,
                freelancer.title,
                freelancer.category,
                freelancer.city,
            ]
        ).lower()
        if search and search not in text:
            continue
        if category and category != freelancer.category:
            continue
        if city and city != freelancer.city:
            continue
        filtered.append(freelancer)

    categories = merge_options(SERVICE_CATEGORIES, all_freelancers, "category")
    cities = merge_options(KOSOVO_CITIES, all_freelancers, "city")
    return render_template(
        "freelancers.html",
        freelancers=filtered,
        categories=categories,
        cities=cities,
        selected_search=request.args.get("search", ""),
        selected_category=category,
        selected_city=city,
    )


@public_bp.route("/freelancer/<int:freelancer_id>")
def freelancer_detail_by_id(freelancer_id):
    freelancer = get_freelancer_by_id(freelancer_id)
    return render_template("freelancer-detail.html", freelancer=freelancer)


@public_bp.route("/freelancer-detail.html")
def freelancer_detail():
    freelancer_id = request.args.get("id", type=int)
    freelancer = get_freelancer_by_id(freelancer_id) if freelancer_id else None
    return render_template("freelancer-detail.html", freelancer=freelancer)


@public_bp.route("/media/<storage_key>")
def uploaded_media(storage_key):
    image = UploadedImage.query.filter_by(storage_key=storage_key).first()
    if image is None:
        abort(404)

    return send_file(
        BytesIO(image.data),
        mimetype=image.mime_type,
        download_name=image.original_filename or f"{storage_key}.bin",
        max_age=31536000,
    )


@public_bp.route("/kontakto", methods=["GET", "POST"])
@public_bp.route("/kontakto.html", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not validate_contact_form(request.form):
            flash("Ju lutem plotësoni të gjitha fushat e kontaktit.", "error")
            return redirect(url_for("public.contact"))
        create_message(request.form)
        flash("Mesazhi u dërgua me sukses.", "success")
        return redirect(url_for("public.contact"))
    return render_template("kontakto.html")


@public_bp.route("/sherbimet")
@public_bp.route("/sherbimet.html")
def services():
    return render_template("sherbimet.html")


@public_bp.route("/rreth-nesh")
@public_bp.route("/rreth-nesh.html")
def about():
    return render_template("rreth-nesh.html")
