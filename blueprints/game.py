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


@game.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('game/game.html')
    elif request.method == 'POST':
        return '', 200


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

@game.route('/gameplay', methods=['GET'])
def get_game():
        if request.method == 'GET':
            return render_template('game/play_game.html')