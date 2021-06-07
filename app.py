from flask import Flask
from flask_login import LoginManager

from blueprints.main import main
from blueprints.auth import auth
from blueprints.game import game
from blueprints.stats import stats
from models.database import db

app = Flask(__name__)
app.secret_key = b'\xf3\xd8\xbdU\xf40HT3\x02\xcb\x8d\x9eO\xce\x8a.\xa5E\xec1\xe0\x16\xba'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mastermind.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(game, url_prefix='/games')
app.register_blueprint(stats, url_prefix='/stats')

db.init_app(app)

lm = LoginManager()
lm.login_view = 'auth.login'
lm.init_app(app)

from models.user import User
from models.game import COLORS
from models.color import Color


def fill_colors():
    for color in COLORS:
        db.session.add(Color(color))
    db.session.commit()


with app.app_context():
    db.drop_all()
    db.create_all()
    fill_colors()


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
