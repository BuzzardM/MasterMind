from models.database import db


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String)

    def __init__(self, color):
        self.color = color
