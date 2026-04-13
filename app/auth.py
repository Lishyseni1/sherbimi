from functools import wraps

from flask import redirect, session, url_for

from .models import AdminUser


def authenticate_admin(username, password):
    admin = AdminUser.query.filter_by(username=username).first()
    return bool(admin and admin.check_password(password))


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapped_view
