from app import db
from datetime import datetime

ROLE_USER = 0
ROLE_OFFICIAL = 1
ROLE_ADMIN = 2

SCOPE_COLLAGE = 0
SCOPE_CAMPUS = 1
SCOPE_ALL = 2

MALE = 0
FEMALE = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), nullable = False, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    avatar = db.Column(db.String(40))
    annoucements = db.relationship('Annoucement', backref = 'owner', \
            lazy = 'dynamic')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Annoucement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True)
    topic = db.Column(db.String(40))
    summary = db.Column(db.String(500))
    poster = db.Column(db.String(40))
    rdate = db.Column(db.DateTime, default = datetime.now)
    addr = db.Column(db.String(80))
    sdate = db.Column(db.DateTime)
    scope = db.Column(db.SmallInteger, default = SCOPE_COLLAGE)
    host = db.Column(db.String(80))
    undertaker = db.Column(db.String(80))
    sponsor = db.Column(db.String(80))
    contact = db.Column(db.String(500))
    remark = db.Column(db.String(500))
    form = db.Column(db.String(40))
    qna = db.Column(db.String(500))
    accept_apply = db.Column(db.Boolean, default = False)
    deleted = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    applicants = db.relationship('Apply', backref = 'annoucement',\
            lazy = 'dynamic')

    def __repr__(self):
        return '<Annoucement %r>' % (self.name)

class Apply(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    annoucement_id = db.Column(db.Integer,db.ForeignKey('annoucement.id'))
    name = db.Column(db.String(20))
    sex = db.Column(db.SmallInteger, default = MALE)
    collage = db.Column(db.String(40))
    major = db.Column(db.String(40))
    no_student = db.Column(db.String(20))
    contact = db.Column(db.String(500))

    def __repr__(self):
        return '<Apply> %r' % (self.name)
