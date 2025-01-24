from typing import Final
from flask import Blueprint, render_template, session
from app.models.user import User


home: Final[Blueprint] = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
@home.route('/home', methods=['GET'])
def index() -> str:
	time: str = '00:10'
	if 'user_id' in session:
		user: User = User.get_by_id(session['user_id'])
		time = user.custom_pomodoro_time

	# For testing purposes
	time = '00:10'

	return render_template('home.html', time=time)
