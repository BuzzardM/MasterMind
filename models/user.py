from flask_login import UserMixin

from models.database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    games = db.relationship('Game', backref='user', lazy=True)

    def __init__(self, username, password, name):
        self.password = password
        self.name = name
        self.username = username
