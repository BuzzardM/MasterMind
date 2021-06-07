import random

from models.color import Color
from models.colors_in_game import colors_in_game
from models.database import db

COLORS = ['Red', 'Yellow', 'White', 'Brown', 'Blue', 'Black', 'Pink', 'Purple', 'Green', 'Orange']
MIN_POS = 4
MAX_POS = 10


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    colors = db.relationship(Color, secondary=colors_in_game)
    amount_of_positions = db.Column(db.Integer)
    duplicate_colors = db.Column(db.Boolean)
    score = db.Column(db.Integer)
    guesses = db.Column(db.Integer)
    code = db.Column(db.String(500))

    def __init__(self):
        self.guesses = 0

    def initialize_new_game(self):
        return

    def create_new_code(self):
        code = []
        colors = self.colors

        while len(code) < self.amount_of_positions:
            entry = random.choice(self.colors)
            code.append(entry)
            if self.duplicate_colors is False:
                colors.remove(entry)

        print(code)
