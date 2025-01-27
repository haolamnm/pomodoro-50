from typing import Final
from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models.user import User
from app.utils.types import RenderResponse, RedirectResponse
from app.utils.decorators import login_required
from app.forms.settings import DurationSettingsForm


settings: Final[Blueprint] = Blueprint('settings', __name__)


@settings.route('/', methods=['GET', 'POST'])
@settings.route('/me', methods=['GET', 'POST'])
@login_required
def me() -> RenderResponse | RedirectResponse:
	form: DurationSettingsForm = DurationSettingsForm()

	if form.validate_on_submit():
		user_id: int = session['user_id']
		user: User = User.get_by_id(user_id)
		duration: str = form.duration.data
		user.update_custom_pomodoro_time(duration)
		flash('Settings updated successfully', 'success')
		return redirect(url_for('settings.me')), 301

	return render_template('settings.html', form=form), 200
