from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SECRET_KEY'] = '7fd1296cc2172fe50e424c5f71837bc6'
login_manager = LoginManager(app)
db = SQLAlchemy(app)

from Ogloszenia24 import views
