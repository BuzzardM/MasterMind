from models.database import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    turn = db.Column(db.Integer)
    perfect_guesses = db.Column(db.Integer)
    good_guesses = db.Column(db.Integer)
    incorrect_guesses = db.Column(db.Integer)
