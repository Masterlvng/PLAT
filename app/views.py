from flask import g, render_template, request, abort
from app import app, db
from utils import current_user, logout_user, load_user_by_name,\
        load_user_by_email, remember_user,Role_required, annoucement_exist,\
        check_annoucement_path, AlchemyEncoder, load_ann_by_name
from forms import LoginForm, AnnoucementForm
from models import ROLE_USER, ROLE_OFFICIAL, ROLE_ADMIN,\
        Annoucement
from werkzeug import secure_filename

import os
import json

@app.before_request
def before_request():
    g.user = current_user()


@app.route('/login', methods=['GET','POST'])
def login():
    if g.user != None:
        return 'logined!'
    form = LoginForm()
    if form.validate_on_submit():
        user = None
        if '@' in form.account.data:
            user = load_user_by_email(form.account.data)
        else:
            user = load_user_by_name(form.account.data)
        if user is not None:
            remember_user(user)
            return 'success!'
        else:
            return 'error!'
    return render_template('extend.html',form=form)



@app.route('/logout', methods=['GET'])
def logout():
    logout_user()

@app.route('/issue/annoucement',methods=['GET','POST'])
@Role_required(ROLE_OFFICIAL)
def issue_annoucement():
    form = AnnoucementForm()
    form_name, poster_name = None, None
    if form.validate_on_submit():
        if annoucement_exist(form.name.data):
            return 'name exists!'
        if form.accept_apply.data == 1:
            annouce_dir = os.path.join(app.config['APPLICANT_DIR'],form.name.data)
            os.mkdir(annouce_dir)
            if form.form.file is not None:
                form_name = form.name.data +'.'+form.form.file.filename.split('.')[-1]
                form_path = os.path.join(app.config['FORMS_DIR'],\
                    form_name)
                form.form.file.save(form_path)

        if form.poster.file is not None:
            poster_name = form.name.data +'.'+ form.poster.data.filename.split('.')[-1]
            poster_path = os.path.join(app.config['POSTER_DIR'],\
                    poster_name)
            form.poster.file.save(poster_path)
        ann = Annoucement(name=form.name.data,\
                topic=form.topic.data,\
                summary=form.summary.data,\
                poster=poster_name,\
                addr=form.addr.data,\
                sdate=form.sdate.data,\
                scope=form.scope.data,\
                host=form.host.data,\
                undertaker=form.undertaker.data,\
                sponsor=form.sponsor.data,\
                contact=form.contact.data,\
                remark=form.remark.data,\
                form=form_name,\
                qna=form.qna.data,\
                accept_apply=form.accept_apply.data,\
                user_id=g.user.id)
        db.session.add(ann)
        db.session.commit()
        return 'success!'
    return str(form.errors)


@app.route('/<official>/<ann>',methods=['GET','POST'])
@check_annoucement_path
def annoucement(official,ann):
    '''
    if GET then return ann in json format
    if POST ,it means that someone apply
    '''
    if request.method == 'GET':
        user = load_user_by_name(official)
        annoucement = load_ann_by_name(ann)
        if annoucement.owner == user:
            return json.dumps(annoucement, cls=AlchemyEncoder)
        abort(404)
    elif request.method == 'POST':
        pass
    abort(403)

@app.route('/<official>')
def offcial(official):
    pass

@app.route('/user/<name>')
def profile(name):
    pass
