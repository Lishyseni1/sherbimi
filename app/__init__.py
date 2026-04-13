import os

from flask import Flask

from .extensions import db, migrate


def _normalize_database_url(url):
    if not url:
        return "sqlite:///app.db"
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def create_app():
    app = Flask(__name__, template_folder="..", static_folder="../static")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-simple-secret-key")
    app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
    app.config["SQLALCHEMY_DATABASE_URI"] = _normalize_database_url(os.getenv("DATABASE_URL"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import public_bp
    from .admin_routes import admin_bp
    from .services import bootstrap_database, ensure_upload_directories

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        ensure_upload_directories(app.config["UPLOAD_FOLDER"])
        bootstrap_database()

    return app
