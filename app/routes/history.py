from typing import Final
from flask import Blueprint, render_template, session
from app.models import Pomodoro
from app.utils.decorators import login_required


history: Final[Blueprint] = Blueprint('history', __name__)


@history.route('/', methods=['GET'])
@history.route('/me', methods=['GET'])
@login_required
def me() -> str:
	user_id: int = session['user_id']
	pomodoros: list[Pomodoro] = Pomodoro.get_by_user_id(user_id, 'desc')

	return render_template('history.html', pomodoros=pomodoros)
