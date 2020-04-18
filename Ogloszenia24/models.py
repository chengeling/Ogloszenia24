from Ogloszenia24 import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from Ogloszenia24 import app

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    adverts = db.relationship('Advert', backref='autor', lazy=True)
    messages_sent = db.relationship('Message',foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    telephone = db.Column(db.String(15))

    def __repr__(self):
        return f"Uzytkownik('{self.username}', '{self.email}'"


class Advert(db.Model):
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer)
    city = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Ogloszenie('{self.title}', '{self.date}', '{self.category}')"
        
class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    advert_title = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Wiadomosc('{self.body}')"
