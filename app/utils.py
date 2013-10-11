from flask import session, abort, g, request, current_app
from functools import wraps, update_wrapper
from app.models import User,Annoucement,ROLE_OFFICIAL
from app import db
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from datetime import datetime
from sqlalchemy import and_

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
                    if isinstance(data,datetime):
                        fields[field] = str(data)
                    else:
                        fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)

def mod_obj_by_json(obj,json,value_dont_changed):
    if not isinstance(json,dict):
        return NotImplemented
    for field in [ key for key in json if key in dir(obj) and \
            key not in value_dont_changed ]:
        obj.__setattr__(field,json[field])

def load_user_by_id(id):
    return User.query.filter(User.id==id).first()

def load_user_by_name(name):
    return User.query.filter(User.nickname==name).first()

def load_user_by_email(email):
    return User.query.filter(User.email==email).first()

def load_offi_by_name(name):
    return User.query.filter(and_(User.nickname==name,User.role==ROLE_OFFICIAL)).first()

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

def seek_ones_ann(user,start,offset,order=0):
    '''
    when order = 0 means order by rdate,
    1 means order by sdate
    '''
    if  not isinstance(user,User):
        return
    if offset > 20:
        offset = 20
    if start == 0 and order == 0:
        return Annoucement.query.filter(Annoucement.user_id==user.id).\
                order_by('rdate desc').limit(offset)
    elif start == 0 and order == 1:
        return Annoucement.query.filter(Annoucement.user_id==user.id).\
                order_by('sdate desc').limit(offset)
    ann = Annoucement.query.filter(Annoucement.id==start).first()
    if ann is None:
        return None
    if order == 0:
        return Annoucement.query.filter( and_(Annoucement.user_id==user.id,\
                Annoucement.rdate < ann.rdate)).order_by('rdate desc').limit(offset)
    else:
        return Annoucement.query.filter( and_(Annoucement.user_id==user.id,\
                Annoucement.sdate < ann.sdate)).order_by('sdate desc').limit(offset)

def seek_all_ann(start,offset):
    pass

def user_exist(name):
    return User.query.filter(User.nickname==name).count() > 0

def check_annoucement_path(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        official, ann = request.path.split('/')[-2:]
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

def require_ann_owner(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        if g.user is None:
            return 'please login!'
        ann_name = request.path.split('/')[-1]
        ann = load_ann_by_name(ann_name)
        if ann.owner == g.user:
            return fn(*args,**kwargs)
        return 'no permission!'
    return decorator

