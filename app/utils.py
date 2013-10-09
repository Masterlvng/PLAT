from flask import session, abort, g, request, current_app
from functools import wraps, update_wrapper
from app.models import User,Annoucement
from app import db
from sqlalchemy.ext.declarative import DeclarativeMeta
import json


class AlchemyEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and \
                    x not in ['metadata','query','query_class'] ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)

def load_user_by_id(id):
    return User.query.filter(User.id==id).first()

def load_user_by_name(name):
    return User.query.filter(User.nickname==name).first()

def load_user_by_email(email):
    return User.query.filter(User.email==email).first()

def load_ann_by_name(name):
    return Annoucement.query.filter(Annoucement.name==name).first()

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
            if current_user() is None:
                return 'need to login!'
            elif current_user().role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return update_wrapper(wrapped_func,fn)
    return decorator

def annoucement_exist(name):
    return Annoucement.query.filter(Annoucement.name==name).count() > 0

def user_exist(name):
    return User.query.filter(User.nickname==name).count() > 0

def check_annoucement_path(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        official, ann = request.path.split('/')[1:]
        '''
        if not user_exist(user):
            return 'user not exist'
        if not annoucement_exist(ann):
            return 'ann not exist'
        '''
        user = load_user_by_name(official)
        annoucement = load_ann_by_name(ann)
        if user == annoucement.owner:
            return fn(*args, **kwargs)
        abort(404)
    return decorator
