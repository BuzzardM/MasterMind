from models.database import db


class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    turn = db.Column(db.Integer, db.Sequence('turn_seq', start=1, increment=1))
    guess = db.Column(db.String(500))
