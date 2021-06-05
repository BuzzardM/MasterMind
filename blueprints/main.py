from flask import Blueprint, request, render_template

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('main/index.html')
