from typing import Final
from flask import Blueprint, flash, redirect, url_for, render_template, session
from flask_mail import Message
from app.forms.profile import (
	UpdateEmailForm,
	UpdatePasswordForm,
	DeleteProfileForm,
	ResetPasswordRequestForm,
	ResetPasswordTokenForm
)
from app.models import User, Pomodoro
from app.utils.types import DurationLog, RenderResponse, RedirectResponse
from app.utils.helpers import get_all_time_duration
from app.utils.decorators import login_required
from app.utils.extensions import mail


profile: Final[Blueprint] = Blueprint('profile', __name__)


@profile.route('/', methods=['GET'])
@profile.route('/me', methods=['GET'])
@login_required
def me() -> RenderResponse:
	user_id: int = session['user_id']
	user: User = User.get_by_id(user_id)
	pomodoros: list[Pomodoro] = Pomodoro.get_by_user_id(user_id)
	all_time_duration_logs: list[DurationLog] = get_all_time_duration(pomodoros)
	return render_template(
		'profile/me.html',
		user=user,
		all_time_duration_logs=all_time_duration_logs
	), 200


@profile.route('/update/email', methods=['GET', 'POST'])
@login_required
def update_email() -> RenderResponse | RedirectResponse:
	user: User = User.get_by_id(session['user_id'])
	form: UpdateEmailForm = UpdateEmailForm(user=user)

	if form.validate_on_submit():
		user.email = str(form.new_email.data)
		user.update()
		user.set_session()
		flash('Email updated successfully', 'success')
		return redirect(url_for('profile.me')), 301

	return render_template('profile/update_email.html', form=form), 200


@profile.route('/update/password', methods=['GET', 'POST'])
@login_required
def update_password() -> RenderResponse | RedirectResponse:
	user: User = User.get_by_id(session['user_id'])
	form: UpdatePasswordForm = UpdatePasswordForm(user=user)

	if form.validate_on_submit():
		user.set_password(str(form.new_password.data))
		user.update()
		flash('Password updated successfully', 'success')
		return redirect(url_for('profile.me')), 301

	return render_template('profile/update_password.html', form=form), 200


@profile.route('/delete', methods=['GET', 'POST'])
def delete() -> RenderResponse | RedirectResponse:
	user: User = User.get_by_id(session['user_id'])
	form: DeleteProfileForm = DeleteProfileForm(user=user)

	if form.validate_on_submit():
		user.delete()
		session.clear()
		flash('Profile deleted successfully', 'success')
		return redirect(url_for('home.index')), 301

	return render_template('profile/delete.html', form=form), 200


@profile.route('/reset/password/request', methods=['GET', 'POST'])
def reset_password_request() -> RenderResponse | RedirectResponse:
	form: ResetPasswordRequestForm = ResetPasswordRequestForm()
	if form.validate_on_submit():
		msg: Message = form.user.create_reset_password_email()
		mail.send(msg)
		flash('Reset email sent', 'success')
		return redirect(url_for('login.email')), 301

	return render_template(
		'profile/reset_password_request.html',
		form=form
	), 200


@profile.route('/reset/password/<string:token>', methods=['GET', 'POST'])
def reset_password_token(token: str) -> RenderResponse | RedirectResponse:
	try:
		user: User = User.verify_token(token)

	except ValueError:
		flash('Token is invalid', 'danger')
		return redirect(url_for('profile.reset_password_request')), 301

	form: ResetPasswordTokenForm = ResetPasswordTokenForm()
	if form.validate_on_submit():
		user.set_password(str(form.password.data))
		user.update()
		flash('Reset password successfully', 'success')
		return redirect(url_for('login.email')), 301

	return render_template('profile/reset_password_token.html', token=token, form=form), 200
