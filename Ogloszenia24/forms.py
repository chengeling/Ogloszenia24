from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Length, Regexp
from Ogloszenia24.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Nazwa użytkownika", render_kw={"placeholder": "Nazwa użytkownika"}, validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email", render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email(message="Zły format adresu email")])
    password = PasswordField("Hasło", render_kw={"placeholder": "Hasło"}, validators=[DataRequired(), Length(min=6, max=30 , message="Hasło powinno mieć od 6 do 30 znaków")])
    confirm_password = PasswordField("Potwierdź hasło", render_kw={"placeholder": "Potwierdź hasło"}, validators=[DataRequired(), EqualTo('password', message="Hasła się nie zgadzają.")])
    submit = SubmitField("Zarejestruj się")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Podana nazwa użytkownika jest zajęta. Spróbuj ponownie')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Podany adres email jest zajęty. Spróbuj ponownie')

class UpdateAccountForm(FlaskForm):
    username = StringField("Nazwa użytkownika", validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email(message="Zły format adresu email")])
    telephone = IntegerField("Telefon")
    submit = SubmitField("Rejestracja")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Podana nazwa użytkownika jest zajęta. Spróbuj ponownie')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Podany adres email jest zajęty. Spróbuj ponownie')


class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', render_kw={"placeholder": "Hasło"}, validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Brak konta o podanym adresie email lub błędne hasło')


class AdvertForm(FlaskForm):
    title = StringField('Nazwa ogłoszenia', validators=[DataRequired(), Length(min=10, max=100, message="Nazwa ogłoszenia powinna mieć od 10 do 100 znaków")])
    content = TextAreaField('Treść', validators=[DataRequired(), Length(min=10, max=1000, message="Treść wiadomości powinna mieć od 10 do 1000 znaków")])
    category = SelectField('Kategoria', validators=[DataRequired()], choices=[('motoryzacja','Motoryzacja'), ('nieruchomosci','Nieruchomości'), ('elektronika','Elektronika'), ('praca',
    'Praca'), ('zabawki','Zabawki'), ('odziez','Odzież'), ('obuwie','Obuwie'), ('sport','Sport'), ('silownia','Siłownia'), ('odzywianie','Odżywianie'), ('zabytki','Zabytki'), ('meble','Meble')])
    price = IntegerField('Cena', validators=[DataRequired(message="Zły format ceny")])
    city = StringField('Miasto', validators=[DataRequired(), Regexp('[a-zA-Z]', message="Nazwa miasta musi składać się tylko z liter"), Length(max=50)])
    submit = SubmitField('Dodaj')

class SearchForm(FlaskForm):
    title = StringField('Nazwa ogłoszenia', render_kw={"placeholder": "Wpisz tytuł ogłoszenia..."}, validators=[DataRequired()])
    submit = SubmitField('Szukaj')

class MessageForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    message = TextAreaField('Treść', validators=[DataRequired()])
    submit = SubmitField('Wyślij')
