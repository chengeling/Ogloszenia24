from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import flask_whooshalchemy as whooshalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SECRET_KEY'] = '7fd1296cc2172fe50e424c5f71837bc6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WHOOSH_BASE'] = 'whoosh'
login_manager = LoginManager(app)
login_manager.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
from Ogloszenia24 import views
