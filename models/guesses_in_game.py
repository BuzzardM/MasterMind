from models.database import db

guesses_in_game = db.Table(
    'guesses_in_game',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('guess_id', db.Integer, db.ForeignKey('guess.id'), primary_key=True)
)
