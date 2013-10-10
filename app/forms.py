from flask_wtf import Form

from flask_wtf.file import FileAllowed, FileField
from wtforms import TextField, PasswordField, DateField, IntegerField,\
        BooleanField

from wtforms.validators import Required, AnyOf
from app.models import SCOPE_CAMPUS, SCOPE_ALL, SCOPE_COLLAGE, MALE, FEMALE

class LoginForm(Form):
    account = TextField('account', validators = [Required()])
    password = PasswordField('password', validators = [Required()])

class AnnoucementForm(Form):
    name = TextField('name',validators = [Required()])
    topic = TextField('topic',validators = [Required()])
    summary = TextField('summary',validators = [Required()])
    poster = FileField('poster', validators = [\
            FileAllowed(['jpg','png'],'jpg,png only!')
            ])
    addr = TextField('addr',validators = [Required()])
    sdate = DateField('sdate',validators = [Required()])
    scope = IntegerField('scope',validators = [AnyOf([SCOPE_CAMPUS,SCOPE_ALL,\
            SCOPE_COLLAGE])])
    host = TextField('host', validators = [Required()])
    undertaker = TextField('undertaker', validators = [Required()])
    sponsor = TextField('sponsor')
    contact = TextField('contact')
    remark = TextField('remark')
    form = FileField('form', validators = [\
            FileAllowed(['doc','docx'],'doc,docx only!')])
    qna = TextField('qna')
    accept_apply = IntegerField('accept_apply', validators = [AnyOf([0,1])])

class Mod_Form(Form):
    form = FileField('form', validators = [\
            FileAllowed(['doc','docx'],'doc,docx only!')])

class Mod_Poster(Form):
    poster = FileField('poster', validators = [\
            FileAllowed(['jpg','png'],'jpg,png only!')])

class Apply_Form(Form):
    name = TextField('name', validators = [Required()])
    sex = IntegerField('sex', validators = [AnyOf([MALE,FEMALE])])
    collage = TextField('collage')
    major = TextField('major')
    no_student = TextField('no_student')
    contact = TextField('contact', validators = [Required()])
    form = FileField('form', validators = [\
            FileAllowed(['doc','docx'],'doc,docx only!')])


