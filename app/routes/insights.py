from typing import Final
from flask import Blueprint, render_template, session
from datetime import datetime, time, timedelta, date
from app.models.pomodoro import Pomodoro
from app.utils.types import RenderResponse
from app.utils.helpers import get_weekly_duration
from app.utils.decorators import login_required


insights: Final[Blueprint] = Blueprint('insights', __name__)


@insights.route('/', methods=['GET'])
@insights.route('/me', methods=['GET'])
@login_required
def me() -> RenderResponse:
	# Get the first day and start time of the week
	start_of_week: date = datetime.now().date() - timedelta(days=datetime.now().weekday())
	start_at = datetime.combine(start_of_week, time.min)

	# Get the last day and end time of the week
	end_of_week: date = start_of_week + timedelta(days=6)
	end_at = datetime.combine(end_of_week, time.max)

	# Get all pomodoros in that week
	user_id: int = session['user_id']
	pomodoros: list[Pomodoro] = Pomodoro.get_by_time(user_id, start_at, end_at)

	# Get weekly duration
	durations: list[int] = [pomodoro.duration for pomodoro in pomodoros]
	start_ats: list[datetime] = [pomodoro.start_at for pomodoro in pomodoros]
	weekly_durations: dict[str, int] = get_weekly_duration(durations, start_ats)

	return render_template(
		'insights.html',
		weekly_durations=weekly_durations
	), 200
