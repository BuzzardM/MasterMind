from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

from models.user import User

stats = Blueprint('stats', __name__)


@stats.before_request
def check_login():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))


@stats.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        completed_games = [game for game in current_user.games if game.completed is True]
        cheated_games = [game for game in current_user.games if game.cheat_mode is True]
        total_turns = 0
        for game in current_user.games:
            total_turns += game.current_turn

        return render_template(
            'stats/stats.html',
            user=current_user,
            completed_games=completed_games,
            cheated_games=cheated_games,
            total_turns=total_turns
        )


@stats.route('/', methods=['POST'])
def user_stats():
    if request.method == 'POST':
        username = request.form['username']

        found_user = User.query.filter_by(username=username).first()
        if found_user is None:
            return redirect(url_for('main.index'))

        completed_games = [game for game in found_user.games if game.completed is True]
        cheated_games = [game for game in found_user.games if game.cheat_mode is True]
        total_turns = 0
        for game in found_user.games:
            total_turns += game.current_turn

        return render_template(
            'stats/stats.html',
            user=found_user,
            completed_games=completed_games,
            cheated_games=cheated_games,
            total_turns=total_turns
        )
