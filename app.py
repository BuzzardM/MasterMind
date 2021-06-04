from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/game')
def test():
    return render_template('game.html')


@app.route('/stats')
def stats():
    return render_template('stats.html')


if __name__ == '__main__':
    app.run()
