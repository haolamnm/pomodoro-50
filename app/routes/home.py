from typing import Final
from flask import Blueprint, render_template, session
from app.models.user import User


home: Final[Blueprint] = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
@home.route('/home', methods=['GET'])
def index() -> str:
	#FIXME: Uncomment this code when the User model is implemented
	# if 'user_id' in session:
	# 	user: User = User.get_by_id(session['user_id'])

	# minutes: int = user.custom_pomodoro_time if user else 50
	return render_template('home.html', minutes=50)
