from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

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
def new_game():
    if request.method == 'GET':
       return render_template('game/new_game.html')
