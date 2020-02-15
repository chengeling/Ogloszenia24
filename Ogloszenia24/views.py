from Ogloszenia24 import app, db, bcrypt
from Ogloszenia24.models import User, Advert
from flask import render_template, url_for, flash, redirect
from Ogloszenia24.forms import RegistrationForm, LoginForm, AdvertForm, SearchForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    form = SearchForm()
    return render_template('home.html', form=form)

@app.route('/rejestracja', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password = hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Utworzono nowe konto!")
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dodaj-ogloszenie", methods=['GET', 'POST'])
@login_required
def add_advert():
    form = AdvertForm()
    if form.validate_on_submit():
        advert = Advert(title = form.title.data, content = form.content.data, category = form.category.data, user_id = current_user.get_id())
        db.session.add(advert)
        db.session.commit()
        flash("Pomyślnie dodano ogłoszenie!")
        return redirect(url_for('home'))
    return render_template('advert.html', form=form)
