from Ogloszenia24 import app, db
from Ogloszenia24.models import User, Advert
from flask import render_template, url_for, flash, redirect
from Ogloszenia24.forms import RegistrationForm, LoginForm, AdvertForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rejestracja')
def register():
    form = RegistrationForm()
    if form.validate_on_submit:
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Utworzono nowe konto!")
        redirect (url_for('home'))
    return render_template('register.html', form=form)
