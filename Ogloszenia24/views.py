from Ogloszenia24 import app, db, bcrypt
from Ogloszenia24.models import User, Advert, Message
from flask import render_template, url_for, flash, redirect, abort, request
from Ogloszenia24.forms import RegistrationForm, LoginForm, AdvertForm, UpdateAccountForm, MessageForm, SearchForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/',  methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        tag = "%{}%".format(form.title.data)
        query = Advert.query.filter(Advert.title.like(tag)).all()
        return render_template('search-results.html', query=query)
    new_ads = Advert.query.order_by(Advert.date.desc()).paginate(per_page=5)
    number_of_ads = len(Advert.query.all())
    return render_template('home.html', form=form, number_of_ads = number_of_ads, new_ads = new_ads, title='Ogloszenia24 - najlepsze ogloszenia w sieci!')

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
    return render_template('register.html', form=form, title='Rejestracja')

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
        elif user is None:
            flash("Błędny login lub hasło. Spróbuj ponownie")
    return render_template('login.html', form=form, title='Zaloguj się')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dodaj-ogloszenie/", methods=['GET', 'POST'])
@login_required
def add_advert():
    form = AdvertForm()
    title_form = "Dodaj ogłoszenie"
    user_ads = Advert.query.filter_by(user_id = current_user.id).count()
    if user_ads >= 9:
        flash("Osiągnięto limit ogłoszeń!")
        return redirect(url_for('home'))
    elif form.validate_on_submit():
        advert = Advert(title = form.title.data, content = form.content.data, category = form.category.data, price = form.price.data, city=form.city.data, user_id = current_user.get_id())
        db.session.add(advert)
        db.session.commit()
        flash("Pomyślnie dodano ogłoszenie!")
        return redirect(url_for('home'))
    return render_template('advert.html', form=form, title_form = title_form, title='Dodaj ogłoszenie')

@app.route("/<string:category>/")
def search_results(category):
    page = request.args.get("page", default = 1, type=int)
    ads = Advert.query.filter_by(category = category).order_by(Advert.date.desc()).paginate(per_page=4)
    if ads.total > 0:
        cat = Advert.query.filter_by(category = category).first().category
        return render_template('search.html', ads=ads, cat=cat, title=category.capitalize())
    return render_template('search.html', ads=ads, title=category.capitalize())

@app.route("/ogloszenie/<int:advert_id>/", methods=['POST', 'GET'])
def show_advert(advert_id):
    form = MessageForm()
    advert = Advert.query.get_or_404(advert_id)
    if form.validate_on_submit():
        message = Message(title = form.title.data, body = form.message.data, sender_id = current_user.id, recipient_id = advert.user_id)
        db.session.add(message)
        db.session.commit()
        flash("Pomyślnie wysłano wiadomość")
        return redirect(url_for('home'))
    return render_template('show_ad.html',title = advert.title, form = form, advert=advert)

@app.route("/moje-konto/", methods=['GET', 'POST'])
@login_required
def account():
    user = current_user
    number_of_ads = Advert.query.filter_by(user_id = user.id).count()
    page = request.args.get("page", default = 1, type=int)
    ads = Advert.query.filter_by(user_id = user.id).order_by(Advert.date.desc()).paginate(per_page=3)
    return render_template('user.html', user=user, ads = ads,messages = messages, number_of_ads=number_of_ads, title="Konto użytkownika {}".format(user.username.capitalize()))

@app.route("/moje-konto/wiadomosci", methods=['GET', 'POST'])
@login_required
def messages():
    user = current_user
    #messages_reveived = Message.query.filter_by(recipient_id = user.id)
    #messeges_send = Message.query.filter_by(sender_id = user.id)
    select = request.form.get("mess_select")
    if select == 'send':
        messages = Message.query.filter_by(sender_id = user.id)
    else:
        messages = Message.query.filter_by(recipient_id = user.id)
    return render_template('messages.html', messages=messages)

@app.route("/moje-ogloszenia/<int:advert_id>/edytuj", methods=['GET', 'POST'])
@login_required
def update_advert(advert_id, advert_title):
    advert = Advert.query.get_or_404(advert_id)
    form = AdvertForm()
    title_form = "Edytuj ogłoszenie"
    if form.validate_on_submit():
        advert.title = form.title.data
        advert.content = form.content.data
        advert.category = form.category.data
        advert.price = form.price.data
        advert.city = form.city.data
        db.session.commit()
        flash("Pomyślnie edytowano ogłoszenie!")
        return redirect(url_for('show_advert', advert_id = advert.id))
    return render_template('advert.html', form=form, title_form = title_form, title='Edytuj ogłoszenie')

@app.route("/moje-ogloszenia/<int:advert_id>/usun/")
@login_required
def delete_advert(advert_id):
    advert = Advert.query.get_or_404(advert_id)
    db.session.delete(advert)
    db.session.commit()
    flash("Usunięto ogłoszenie!")
    return redirect(url_for('account'))
