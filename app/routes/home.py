from typing import Final
from flask import Blueprint, render_template, session
from app.models.user import User
from app.utils.types import RenderResponse


home: Final[Blueprint] = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
@home.route('/home', methods=['GET'])
def index() -> RenderResponse:
	if 'user_id' in session:
		user: User = User.get_by_id(session['user_id'])
		time: str = user.custom_pomodoro_time
		return render_template('timer.html', time=time), 200
	else:
		return render_template('home.html'), 200
