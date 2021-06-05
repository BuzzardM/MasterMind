from models.database import db

colors = ["Red", "Yellow", "White", "Brown", "Blue", "Black", "Pink", "Purple", "Green", "Orange"]
min_pos = 4
max_pos = 10


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Add link to player model
    amount_of_colors = db.Column(db.Integer)
    amount_of_positions = db.Column(db.Integer)
    duplicate_colors = db.Column(db.Boolean)
    score = db.column(db.Integer)
