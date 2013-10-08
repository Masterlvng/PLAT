from flask import g, render_template
from app import app
from utils import current_user, logout_user, load_user_by_name,\
        load_user_by_email, remember_user
from forms import LoginForm

@app.before_request
def before_request():
    g.user = current_user()


@app.route('/login', methods=['GET','POST'])
def login():
    if g.user != None:
        print g.user
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

