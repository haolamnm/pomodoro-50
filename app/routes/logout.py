from typing import Final
from flask import Blueprint, url_for, redirect, flash, session
from app.utils.types.route import RedirectResponse


logout: Final[Blueprint] = Blueprint('logout', __name__)


@logout.route('/email', methods=['GET'])
def email() -> RedirectResponse:
	session.pop('user_id', None)
	session.pop('user_email', None)
	# session.clear()
	flash('Logged out successfully', 'success')
	return redirect(url_for('home.index')), 301
