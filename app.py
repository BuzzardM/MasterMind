from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return render_template('invalid_method.html'), 405


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        return render_template('game.html')
    elif request.method == 'POST':
        return '', 200
    else:
        return render_template('invalid_method.html'), 405


@app.route('/stats', methods=['GET'])
def stats():
    if request.method == 'GET':
        return render_template('stats.html')
    else:
        return render_template('invalid_method.html'), 405
