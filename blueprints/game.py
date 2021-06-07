from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

from models.game import COLORS, MIN_POS, MAX_POS, Game

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
        return render_template('game/new_game.html', colors=COLORS, min_pos=MIN_POS, max_pos=MAX_POS)
    if request.method == 'POST':
        positions = request.form.get('positions')
        colors = request.form.getlist('colors')
        duplicate_colors = request.form.get('duplicate_colors')
        cool = Game(colors, positions, duplicate_colors)
        cool.create_new_code()
        return render_template('game/game.html')
