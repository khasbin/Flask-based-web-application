from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect,url_for
import re
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_required, logout_user, login_user, current_user


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
      

auth = Blueprint('auth', __name__)

@auth.get('/login')
@auth.post('/login')
def login():
    if request.method =='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. please enter correct password', catogory = 'error')

        else:
            flash("The username doesnot exits. Please enter correct credentials",category = "error")

    return render_template("login.html", user = current_user)
    


@auth.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.get('/signup')
@auth.post('/signup')
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        username = request.form.get('username')

        user = User.query.filter_by(email = email).first()

        if user:
            flash("The user already exists.", category = 'error')

        elif (re.fullmatch(regex, email)) and (password1 == password2) and len(username)>4:
            new_user = User(email = email, username = username, password = generate_password_hash(password1, method = "sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("The account is created", category = "success")
            return redirect(url_for('auth.login'))
        else:
            flash("The credentials you entered is not valid", category = 'error')

    return  render_template("signup.html",user= current_user)


