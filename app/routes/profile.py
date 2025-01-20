from typing import Final
from flask import Blueprint, flash, redirect, url_for, render_template, session
from flask_mail import Message
from app.forms.profile import ResetPasswordRequestForm, ResetPasswordTokenForm
from app.models.user import User
from app.utils.extensions import mail
from app.utils.types.route import RenderResponse, RedirectResponse


profile: Final[Blueprint] = Blueprint('profile', __name__)


# @profile.route('/<string:username>', methods=['GET'])
# def index(username: str):
# 	return f'Profile: {username}'

@profile.route('reset/password/request', methods=['GET', 'POST'])
def reset_password_request() -> RenderResponse | RedirectResponse:
	if 'user_id' in session:
		flash('Logged in already', 'info')
		return redirect(url_for('home.index')), 301

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


@profile.route('reset/password/<string:token>', methods=['GET', 'POST'])
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
