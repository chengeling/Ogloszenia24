from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Ogloszenia24.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Nazwa użytkownika", render_kw={"placeholder": "Nazwa użytkownika"}, validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email", render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()])
    password = PasswordField("Hasło", render_kw={"placeholder": "Hasło"}, validators=[DataRequired()])
    confirm_password = PasswordField("Potwierdź hasło", render_kw={"placeholder": "Potwierdź hasło"}, validators=[DataRequired(), EqualTo('password')])
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
    email = StringField("Email", validators=[DataRequired(), Email()])
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

class AdvertForm(FlaskForm):
    title = StringField('Nazwa ogłoszenia', validators=[DataRequired()])
    content = TextAreaField('Treść', validators=[DataRequired()])
    category = SelectField('Kategoria', validators=[DataRequired()], choices=[('motoryzacja','Motoryzacja'), ('nieruchomosci','Nieruchomości'), ('elektronika','Elektronika'), ('praca',
    'Praca'), ('zabawki','Zabawki'), ('odziez','Odzież'), ('obuwie','Obuwie'), ('sport','Sport'), ('silownia','Siłownia'), ('odzywianie','Odżywianie'), ('zabytki','Zabytki'), ('meble','Meble')])
    price = IntegerField('Cena', validators=[DataRequired()])
    city = StringField('Miasto', validators=[DataRequired()])
    submit = SubmitField('Dodaj')
    
class MessageForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    message = TextAreaField('Treść', validators=[DataRequired()])
    submit = SubmitField('Wyślij')
