from typing import Final
from flask import Blueprint, render_template


home: Final[Blueprint] = Blueprint('home', __name__)


@home.route('/home', methods=['GET'])
@home.route('/', methods=['GET'])
def index() -> str:
	return render_template('home/index.html')
