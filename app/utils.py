from flask import session, abort
from functools import wraps
from app.models import User
from app import db

def load_user(id):
    return User.query().filter(User.id=id).first()

@property
def current_user():
    return session['user']


def Role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

