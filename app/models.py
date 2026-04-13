from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class AdminUser(TimestampMixin, db.Model):
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)


class Freelancer(TimestampMixin, db.Model):
    __tablename__ = "freelancers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(120), nullable=False, index=True)
    city = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(50), nullable=False, default="")
    whatsapp = db.Column(db.String(255), nullable=False, default="")
    instagram = db.Column(db.String(255), nullable=False, default="")
    address = db.Column(db.String(255), nullable=False, default="")
    image = db.Column(db.String(500), nullable=False)
    premium = db.Column(db.Boolean, nullable=False, default=False, index=True)


class Business(TimestampMixin, db.Model):
    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    category = db.Column(db.String(120), nullable=False, default="")
    city = db.Column(db.String(120), nullable=False, default="")
    description = db.Column(db.Text, nullable=False, default="")
    phone = db.Column(db.String(50), nullable=False, default="")
    email = db.Column(db.String(255), nullable=False, default="")
    website = db.Column(db.String(255), nullable=False, default="")
    address = db.Column(db.String(255), nullable=False, default="")
    image = db.Column(db.String(500), nullable=False, default="")


class ContactMessage(TimestampMixin, db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    @property
    def date(self):
        return self.sent_at.strftime("%Y-%m-%d %H:%M")


class SiteAsset(TimestampMixin, db.Model):
    __tablename__ = "site_assets"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True, nullable=False, index=True)
    value = db.Column(db.String(500), nullable=False, default="")
