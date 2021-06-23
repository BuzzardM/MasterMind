import os

from flask import Blueprint, request, render_template, send_from_directory

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('main/index.html')


@main.route('/favicon.ico', methods=['GET'])
def favicon():
    if request.method == 'GET':
        return send_from_directory(os.path.join(main.root_path, '../static'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')
