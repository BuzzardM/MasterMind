from flask_login import UserMixin

from models.database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    games = db.relationship('Game', backref='user', lazy=True)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
