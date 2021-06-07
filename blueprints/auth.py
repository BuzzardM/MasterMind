from flask import Blueprint, request, render_template, redirect, url_for, flash
import bcrypt
from flask_login import login_user, logout_user

from models.database import db
from models.user import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    elif request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        possible_player = User.query.filter_by(email=email).first()

        if possible_player:
            return redirect(url_for('auth.register'))

        new_player = User(email=email, name=name, password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))

        db.session.add(new_player)
        db.session.commit()

        login_user(new_player)

        return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(password.encode(), user.password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('main.index'))


@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))
