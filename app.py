from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
def test():
    return render_template('game.html')


@app.route('/stats')
def stats():
    return render_template('stats.html')
