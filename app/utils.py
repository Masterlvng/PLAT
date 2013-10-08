from flask import session, abort, g, request, current_app
from functools import wraps, update_wrapper
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
    def decorator(fn):
        def wrapped_func(*args, **kwargs):
            print args,kwargs
            if current_user() is None:
                return 'need to login!'
            elif current_user().role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return update_wrapper(wrapped_func,fn)
    return decorator

def check_annoucement_name(name):
    return Annoucement.query.filter(Annoucement.name==name).count() == 0

