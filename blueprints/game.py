from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

from models.color import Color
from models.database import db
from models.game import MIN_POS, MAX_POS, Game

game = Blueprint('game', __name__)


@game.before_request
def check_login():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))


@game.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('game/game.html')


@game.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        colors = Color.query.all()
        return render_template('game/new_game.html', colors=colors, min_pos=MIN_POS, max_pos=MAX_POS)
    if request.method == 'POST':
        positions: int = request.form.get('positions')
        color_ids = request.form.getlist('colors')
        duplicate_colors: bool = (request.form.get('duplicate_colors') == 'enabled')

        new_game = Game(
            player_id=current_user.id,
            amount_of_positions=positions,
            duplicate_colors=duplicate_colors,
            score=0
        )

        for color_id in color_ids:
            new_game.colors.append(Color.query.filter_by(id=color_id).first())

        new_game.generate_code()

        db.session.add(new_game)
        db.session.commit()

        return render_template('game/game.html')


@game.route('/<game_id>', methods=['GET'])
def get_game(game_id: int):
    if request.method == 'GET':
        playable_game = Game.query.filter_by(id=game_id).first()

        if playable_game is None:
            return redirect(url_for('game.index'))

        return render_template('game/play_game.html')


@game.route('/<game_id>/guess', methods=['POST'])
def make_guess(game_id: int):
    if request.method == 'POST':
        playable_game = Game.query.filter_by(id=game_id).first()

        if playable_game is None:
            return redirect(url_for('game.index'))

        playable_game.guesses.append(Guess())