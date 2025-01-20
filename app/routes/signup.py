from typing import Final
from flask import Blueprint, render_template, url_for, redirect, flash, session
from app.forms.signup import SignupEmailForm
from app.models.user import User
from app.utils.types.route import RedirectResponse, RenderResponse

signup: Final[Blueprint] = Blueprint('signup', __name__)


@signup.route('/email', methods=['GET', 'POST'])
def email() -> RenderResponse | RedirectResponse:
	if 'user_id' in session:
		flash('Logged in already', 'info')
		return redirect(url_for('home.index')), 301

	form: SignupEmailForm = SignupEmailForm()
	if form.validate_on_submit():
		user: User = User(
			email=str(form.email.data),
			raw_password=str(form.password.data)
		)
		user.create()
		flash('Signed up successfully', 'success')
		return redirect(url_for('home.index')), 301

	return render_template('signup.html', form=form), 200
