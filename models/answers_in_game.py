from models.database import db

answers_in_game = db.Table(
    'answers_in_game',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'), primary_key=True)
)
