from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user

from models.answer import Answer
from models.color import Color
from models.database import db
from models.game import MIN_COLORS, MIN_POS, MAX_POS, Game
from models.guess import Guess

game = Blueprint('game', __name__)


@game.before_request
def check_login():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))


@game.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        games = Game.query.filter_by(player_id=current_user.id).all()
        return render_template('game/game.html', games=games)


@game.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        colors = Color.query.all()
        return render_template('game/new_game.html', colors=colors, min_pos=MIN_POS, max_pos=MAX_POS)
    if request.method == 'POST':
        positions = int(request.form.get('positions'))
        color_ids = request.form.getlist('colors')
        duplicate_colors = (request.form.get('duplicate_colors') == 'enabled')
        cheat_mode = (request.form.get('cheat_mode') == 'enabled')

        if len(color_ids) < MIN_COLORS:
            flash('You need to select at least 6 colors!','warning')
            return redirect(url_for('game.new'))

        if duplicate_colors is False and len(color_ids) < positions:
            flash('You need to select as much colors as positions or more!', 'warning')
            return redirect(url_for('game.new'))

        new_game = Game(
            player_id=current_user.id,
            amount_of_positions=positions,
            duplicate_colors=duplicate_colors,
            cheat_mode=cheat_mode,
            current_turn=0,
            completed=False
        )

        for color_id in color_ids:
            new_game.colors.append(Color.query.filter_by(id=color_id).first())

        new_game.generate_code()

        db.session.add(new_game)
        db.session.commit()

        return redirect((url_for('game.get_game', game_id=new_game.id)))


@game.route('/<game_id>', methods=['GET'])
def get_game(game_id: int):
    if request.method == 'GET':
        playable_game = Game.query.filter_by(id=game_id).first()

        if playable_game is None or current_user.id is not playable_game.player_id:
            return redirect(url_for('game.index'))

        return render_template('game/play_game.html', game=playable_game)


@game.route('/<game_id>/guess', methods=['POST'])
def make_guess(game_id: int):
    if request.method == 'POST':
        playable_game = Game.query.filter_by(id=game_id).first()

        if playable_game is None:
            return redirect(url_for('game.index'))

        playable_game.current_turn += 1

        guess = request.form.getlist('guess')

        new_guess = Guess(
            game_id=playable_game.id,
            turn=playable_game.current_turn,
            guess=' '.join(guess)
        )

        perfect_guesses, good_guesses, incorrect_guesses = playable_game.check_guess(guess)

        new_answer = Answer(
            game_id=playable_game.id,
            turn=playable_game.current_turn,
            perfect_guesses=perfect_guesses,
            good_guesses=good_guesses,
            incorrect_guesses=incorrect_guesses
        )

        playable_game.guesses.append(new_guess)
        playable_game.answers.append(new_answer)

        db.session.commit()

        return redirect(url_for('game.get_game', game_id=playable_game.id))


@game.route('/<game_id>/info', methods=['GET'])
def get_game_info(game_id):
    found_game = Game.query.filter_by(id=game_id).first()

    if found_game is None or current_user.id is not found_game.player_id:
        return redirect(url_for('game.index'))

    return render_template('game/info_game.html', game=found_game)
