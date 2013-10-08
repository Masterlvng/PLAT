from flask import session, abort
from functools import wraps
from app.models import User,Annoucement
from app import db

def load_user_by_id(id):
    return User.query.filter(User.id==id).first()

def load_user_by_name(name):
    return User.query.filter(User.nickname==name).first()

def load_user_by_email(email):
    return User.query.filter(User.email==email).first()

def current_user():
    if 'user' not in session:
        return None
    else:
        return session['user']

def logout_user():
    if 'user' in session:
        session.pop('user')

def remember_user(user):
    session['user']=user

def Role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user().role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def check_annoucement_name(name):
    return Annoucement.query.filter(Annoucement.name==name).count() == 0

