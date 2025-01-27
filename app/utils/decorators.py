from functools import wraps
from flask import flash, redirect, session, url_for


def login_required(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if session.get("user_id") is None:
			flash('Please login to access this page', 'warning')
			return redirect(url_for('login.email'))
		return func(*args, **kwargs)

	return decorated_function


# def admin_required(func):
