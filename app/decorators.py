from flask import abort
from functools import wraps
from flask_login import current_user
from .models import Permission, User
from app import login_manager

# decorators to check if the current user has the specified permission and another to check if the
# current user has the admin permission
# login_manager.anonymous_user = AnonymousUser


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if not current_user.is_anonymous:
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function()
    return decorator


# decorator to check for admin permission
def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
