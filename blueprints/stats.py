from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

stats = Blueprint('stats', __name__)


@stats.before_request
def check_login():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))


@stats.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('stats/stats.html', user=current_user)


@stats.route('/<user>', methods=['GET'])
def user_stats(user):
    if request.method == 'GET':
        return render_template('stats/stats.html')
