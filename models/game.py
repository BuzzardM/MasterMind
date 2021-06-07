import random

from models.answer import Answer
from models.answers_in_game import answers_in_game
from models.color import Color
from models.colors_in_game import colors_in_game
from models.database import db
from models.guess import Guess
from models.guesses_in_game import guesses_in_game

COLORS = ['Red', 'Yellow', 'White', 'Brown', 'Blue', 'Black', 'Pink', 'Purple', 'Green', 'Orange']
MIN_POS = 4
MAX_POS = 10


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    colors = db.relationship(Color, secondary=colors_in_game)
    guesses = db.relationship(Guess, secondary=guesses_in_game)
    answers = db.relationship(Answer, secondary=answers_in_game)
    current_turn = db.Column(db.Integer)
    amount_of_positions = db.Column(db.Integer)
    duplicate_colors = db.Column(db.Boolean)
    score = db.Column(db.Integer)
    code = db.Column(db.String(500), nullable=True)

    def generate_code(self):
        code = []
        colors = self.colors

        while len(code) < int(self.amount_of_positions):
            entry = random.choice(self.colors)
            code.append(entry.name)
            if self.duplicate_colors is False:
                colors.remove(entry)

        self.code = ' '.join(code)

    def check_guess(self, guess: []):
        perfect_guesses = 0
        good_guesses = 0

        code = self.code.split(' ')

        remaining_guess = []
        remaining_code = []
        for i in range(len(guess)):
            if guess[i] == code[i]:
                perfect_guesses += 1
            else:
                remaining_guess += guess[i]
                remaining_code += code[i]

        for i in range(len(remaining_guess)):
            if remaining_guess[i] in remaining_code:
                good_guesses += 1
                remaining_code -= remaining_guess[i]

        incorrect_guesses = len(remaining_guess)

        return perfect_guesses, good_guesses, incorrect_guesses
