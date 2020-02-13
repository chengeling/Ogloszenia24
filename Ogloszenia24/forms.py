from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Ogloszenia24.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Nazwa użytkownika", validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Hasło", validators=[DataRequired()])
    confirm_password = StringField("Potwierdź hasło", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Rejestracja")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

class AdvertForm(FlaskForm):
    title = StringField('Nazwa ogłoszenia', validators=[DataRequired()])
    content = TextAreaField('Treść', validators=[DataRequired()])
    submit = SubmitField('Dodaj')
