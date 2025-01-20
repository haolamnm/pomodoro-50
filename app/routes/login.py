from typing import Final
from flask import Blueprint, render_template, url_for, redirect, flash, session
from app.forms.login import LoginEmailForm
from app.utils.types.route import RedirectResponse, RenderResponse


login: Final[Blueprint] = Blueprint('login', __name__)


@login.route('/email', methods=['GET', 'POST'])
def email() -> RenderResponse | RedirectResponse:
	if 'user_id' in session:
		flash('Logged in already', 'info')
		return redirect(url_for('home.index')), 301

	form: LoginEmailForm = LoginEmailForm()
	if form.validate_on_submit():
		form.user.set_session()
		flash('Logged in successfully', 'success')
		return redirect(url_for('home.index')), 301

	return render_template('login.html', form=form), 200
