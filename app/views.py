#!/usr/bin/python
from flask import Flask,render_template,request,session,flash,redirect,url_for,g
#from flask import *
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager,login_user,logout_user,current_user,login_required
from app import app,db,lm
from app.models import User
bootstrap=Bootstrap(app)

@lm.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.before_request
def before_request():
    g.user = current_user




@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    from forms import LoginForm
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            session['email']=form.email.data
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html',form=form,failed_auth=True)
    return render_template('login.html',form=form)

