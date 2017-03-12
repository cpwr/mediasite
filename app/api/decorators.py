import functools

from flask import jsonify
from werkzeug.exceptions import abort

from app import auth


def json():
    """This decorator generates a JSON response from a Python dictionary or
    a SQLAlchemy model."""
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            data = f(*args, **kwargs)
            if isinstance(data, tuple):
                data, status = data
                j = jsonify(data)
                j.status_code = status
                return j
            return jsonify(data)
        return wrapped
    return decorator


def requires_permissions(*permissions):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            user = auth.service.get_user()
            if not user.is_authorized():
                return abort(403)
            if not user.is_admin:
                if not set.intersection(user.get_permissions(), set(permissions)):
                    return abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
