import json
import os
from datetime import datetime
from uuid import uuid4

from flask import current_app
from werkzeug.utils import secure_filename

from .extensions import db
from .models import AdminUser, ContactMessage, Freelancer, SiteAsset

DATA_FOLDER = "data"
FREELANCERS_FILE = os.path.join(DATA_FOLDER, "freelancers.json")
MESSAGES_FILE = os.path.join(DATA_FOLDER, "messages.json")
HOME_BANNER_FILE = os.path.join(DATA_FOLDER, "home_banner.json")
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=600&q=80"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
HOME_BANNER_KEY = "home_banner_image"
KOSOVO_CITIES = [
    "Prishtinë", "Prizren", "Pejë", "Gjakovë", "Gjilan", "Ferizaj", "Mitrovicë", "Podujevë",
    "Vushtrri", "Suharekë", "Rahovec", "Drenas", "Lipjan", "Fushë Kosovë", "Malishevë",
    "Deçan", "Klinë", "Skenderaj", "Istog", "Kaçanik", "Shtime", "Obiliq", "Dragash",
    "Kamenicë", "Viti", "Novobërdë", "Graçanicë", "Hani i Elezit", "Junik", "Mamushë",
]
SERVICE_CATEGORIES = [
    "Zhvillim Web", "Dizajn Grafik", "UI/UX Dizajn", "Marketing Digjital",
    "Menaxhim i Rrjeteve Sociale", "SEO", "Copywriting", "Përkthime",
    "Video Editim", "Fotografi", "Web Designer", "Programim Python",
    "Elektricist", "Hidraulik", "Pastrim Shtëpish", "Pastrim Zyrash",
    "Instalues Kamerash", "Servis Kompjuterësh", "Fotograf Eventesh",
    "Videograf Eventesh", "DJ", "Dekorues Eventesh", "Grimer", "Berber",
    "Trajner Personal", "Babysitter", "Kujdes për të Moshuar",
    "Arkitekt", "Dizajn Interieri", "Konsulencë Marketingu", "Konsulencë Biznesi",
]


def ensure_upload_directories(upload_folder):
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, "banner"), exist_ok=True)


def load_legacy_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return default


def bootstrap_database():
    db.create_all()
    seed_admin_user()
    import_legacy_data()


def seed_admin_user():
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD", "admin123")
    admin = AdminUser.query.filter_by(username=username).first()
    if admin is None:
        admin = AdminUser(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()


def import_legacy_data():
    imported = False

    if Freelancer.query.count() == 0:
        for item in load_legacy_json(FREELANCERS_FILE, []):
            freelancer = Freelancer(
                id=int(item.get("id", 0) or 0) or None,
                name=item.get("name", "").strip(),
                title=item.get("title", "").strip(),
                category=item.get("category", "").strip(),
                city=item.get("city", "").strip(),
                description=item.get("description", "").strip(),
                phone=item.get("phone", "").strip(),
                whatsapp=item.get("whatsapp", "").strip(),
                instagram=item.get("instagram", "").strip(),
                address=item.get("address", "").strip(),
                image=item.get("image", "").strip() or DEFAULT_IMAGE,
                premium=bool(item.get("premium", False)),
            )
            db.session.add(freelancer)
        imported = True

    if ContactMessage.query.count() == 0:
        for item in load_legacy_json(MESSAGES_FILE, []):
            message = ContactMessage(
                id=int(item.get("id", 0) or 0) or None,
                name=item.get("name", "").strip(),
                email=item.get("email", "").strip(),
                subject=item.get("subject", "").strip(),
                message=item.get("message", "").strip(),
                sent_at=parse_legacy_date(item.get("date")),
            )
            db.session.add(message)
        imported = True

    banner = SiteAsset.query.filter_by(key=HOME_BANNER_KEY).first()
    if banner is None:
        data = load_legacy_json(HOME_BANNER_FILE, {"image": ""})
        banner = SiteAsset(key=HOME_BANNER_KEY, value=(data.get("image", "") if isinstance(data, dict) else ""))
        db.session.add(banner)
        imported = True

    if imported:
        db.session.commit()


def parse_legacy_date(value):
    if value:
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    return datetime.utcnow()


def merge_options(defaults, items, attr):
    saved_values = [getattr(item, attr, "") for item in items if getattr(item, attr, "")]
    return sorted(set(defaults + saved_values))


def get_freelancers():
    return Freelancer.query.order_by(Freelancer.premium.desc(), Freelancer.id.desc()).all()


def get_freelancer_by_id(freelancer_id):
    return db.session.get(Freelancer, freelancer_id)


def validate_contact_form(form):
    required_fields = ("name", "email", "subject", "message")
    return all(form.get(field, "").strip() for field in required_fields)


def validate_freelancer_form(form):
    required_fields = ("name", "title", "category", "city", "description")
    return all(form.get(field, "").strip() for field in required_fields)


def create_freelancer_from_form(form, file=None, existing=None):
    existing = existing or Freelancer(image=DEFAULT_IMAGE)
    freelancer = existing if isinstance(existing, Freelancer) else Freelancer()
    previous_image = freelancer.image
    uploaded_image = save_upload(file)
    image = uploaded_image or form.get("image", "").strip() or previous_image or DEFAULT_IMAGE

    freelancer.name = form.get("name", "").strip()
    freelancer.title = form.get("title", "").strip()
    freelancer.category = form.get("category", "").strip()
    freelancer.city = form.get("city", "").strip()
    freelancer.description = form.get("description", "").strip()
    freelancer.phone = form.get("phone", "").strip()
    freelancer.whatsapp = form.get("whatsapp", "").strip()
    freelancer.instagram = form.get("instagram", "").strip()
    freelancer.address = form.get("address", "").strip()
    freelancer.image = image
    freelancer.premium = form.get("premium") == "on"

    if uploaded_image and previous_image and previous_image != uploaded_image and previous_image.startswith("/static/"):
        delete_uploaded_file(previous_image)

    return freelancer


def save_freelancer(freelancer):
    db.session.add(freelancer)
    db.session.commit()
    return freelancer


def delete_freelancer(freelancer):
    if freelancer.image and freelancer.image.startswith("/static/"):
        delete_uploaded_file(freelancer.image)
    db.session.delete(freelancer)
    db.session.commit()


def get_messages():
    return ContactMessage.query.order_by(ContactMessage.id.desc()).all()


def create_message(form):
    message = ContactMessage(
        name=form.get("name", "").strip(),
        email=form.get("email", "").strip(),
        subject=form.get("subject", "").strip(),
        message=form.get("message", "").strip(),
    )
    db.session.add(message)
    db.session.commit()
    return message


def delete_message(message):
    db.session.delete(message)
    db.session.commit()


def get_home_banner():
    asset = SiteAsset.query.filter_by(key=HOME_BANNER_KEY).first()
    if asset is None:
        asset = SiteAsset(key=HOME_BANNER_KEY, value="")
        db.session.add(asset)
        db.session.commit()
    return {"image": asset.value or ""}


def set_home_banner(image_path):
    asset = SiteAsset.query.filter_by(key=HOME_BANNER_KEY).first()
    if asset is None:
        asset = SiteAsset(key=HOME_BANNER_KEY)
        db.session.add(asset)
    asset.value = image_path
    db.session.commit()


def save_upload(file):
    return save_upload_to_folder(file, "")


def save_upload_to_folder(file, subfolder):
    if not file or not file.filename:
        return ""

    filename = secure_filename(file.filename)
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        return ""

    unique_name = f"{uuid4().hex}_{filename}"
    base_upload_folder = current_app.config["UPLOAD_FOLDER"]
    disk_path = os.path.join(base_upload_folder, *(subfolder.split(os.sep) if subfolder else []), unique_name)
    os.makedirs(os.path.dirname(disk_path), exist_ok=True)
    file.save(disk_path)

    path_parts = ["static", "uploads"]
    if subfolder:
        path_parts.extend(subfolder.replace("\\", "/").strip("/").split("/"))
    path_parts.append(unique_name)
    return "/" + "/".join(path_parts)


def save_home_banner_upload(file):
    uploaded_image = save_upload_to_folder(file, "banner")
    if not uploaded_image:
        return ""
    delete_uploaded_file(get_home_banner().get("image", ""))
    set_home_banner(uploaded_image)
    return uploaded_image


def clear_home_banner():
    delete_uploaded_file(get_home_banner().get("image", ""))
    set_home_banner("")


def delete_uploaded_file(image_path):
    if not image_path or not image_path.startswith("/static/"):
        return

    relative_path = image_path.replace("/static/", "", 1).replace("/", os.sep)
    file_path = os.path.join("static", relative_path)
    if os.path.exists(file_path):
        os.remove(file_path)
