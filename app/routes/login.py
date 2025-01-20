from typing import Final, Any
from flask import current_app as app
from flask import Blueprint, render_template, url_for, redirect, flash, session
from app.models import User
from app.forms.login import LoginEmailForm, LoginGoogleForm, LoginGitHubForm
from app.utils.extensions import oauth
from app.utils.exceptions import UserEmailNotFoundError
from app.utils.types.route import RedirectResponse, RenderResponse


login: Final[Blueprint] = Blueprint('login', __name__)


@login.route('/email', methods=['GET', 'POST'])
def email() -> RenderResponse | RedirectResponse:
	if 'user_id' in session:
		flash('Logged in already', 'info')
		return redirect(url_for('home.index')), 301

	login_email_form: LoginEmailForm = LoginEmailForm()
	login_google_form: LoginGoogleForm = LoginGoogleForm()
	login_github_form: LoginGitHubForm = LoginGitHubForm()

	if (login_email_form.validate_on_submit()
	 	and login_email_form.form_name.data == 'login_email_form'):
		login_email_form.user.set_session()
		flash('Logged in successfully', 'success')
		return redirect(url_for('home.index')), 301

	if (login_google_form.validate_on_submit()
	 	and login_google_form.form_name.data == 'login_google_form'):
		return redirect(url_for('login.google')), 302

	if (login_github_form.validate_on_submit()
	 	and login_github_form.form_name.data == 'login_github_form'):
		return redirect(url_for('login.github')), 302

	return render_template(
		'login.html',
		login_email_form=login_email_form,
		login_google_form=login_google_form,
		login_github_form=login_github_form,
	), 200


@login.route('/google', methods=['GET', 'POST'])
def google() -> RedirectResponse:
	try:
		redirect_uri: str = url_for('login.google_authorize', _external=True)
		client: Any = oauth.create_client('google')
		if client is None:
			raise ValueError('Failed to create OAuth client for Google')
		return client.authorize_redirect(redirect_uri), 302

	except (ValueError, Exception) as e:
		flash('Logged in with Google failed', 'danger')
		app.logger.error(f'[ERROR] {e}')
		return redirect(url_for('login.email')), 302


@login.route('/google/authorize', methods=['GET'])
def google_authorize() -> RedirectResponse:
	try:
		client: Any = oauth.create_client('google')
		if client is None:
			raise ValueError('Failed to create OAuth client for Google')
		client.authorize_access_token()
		userinfo_endpoint = client.server_metadata['userinfo_endpoint']
		response = client.get(userinfo_endpoint)
		userinfo = response.json()

		email: Final[str] = userinfo['email']
		oauth_token: Final[str] = userinfo['sub']
		oauth_provider: Final[str] = 'google'

		user: User = User.get_by_email(email)
		if user.oauth_provider != oauth_provider or user.oauth_token != oauth_token:
			user.oauth_token = oauth_token
			user.oauth_provider = oauth_provider
			user.update()

		user.set_session()
		flash('Logged in with Google successfully', 'success')
		return redirect(url_for('home.index')), 302

	except UserEmailNotFoundError:
		new_user: User = User(
			email=email,
			raw_password=None,
			oauth_token=oauth_token,
			oauth_provider=oauth_provider
		)
		new_user.create()
		new_user.set_session()
		flash('Signed up with Google successfully', 'success')
		return redirect(url_for('home.index')), 302

	except (ValueError, Exception) as e:
		flash('Authorization with Google failed', 'danger')
		app.logger.error(f'[ERROR] {e}')
		return redirect(url_for('login.email')), 302


@login.route('/github', methods=['POST'])
def github() -> RedirectResponse:
	try:
		redirect_uri: str = url_for('login.github_authorize', _external=True)
		client: Any = oauth.create_client('github')
		if client is None:
			raise ValueError('Failed to create OAuth client for GitHub')
		return client.authorize_redirect(redirect_uri), 302

	except (ValueError, Exception) as e:
		flash('Logged in with GitHub failed', 'danger')
		app.logger.error(f'[ERROR] {e}')
		return redirect(url_for('login.email')), 302


@login.route('/github/authorize', methods=['GET'])
def github_authorize() -> RedirectResponse:
	try:
		client: Any = oauth.create_client('github')
		if client is None:
			raise ValueError('Failed to create OAuth client for GitHub')
		client.authorize_access_token()
		response = client.get('user').json()

		email: Final[str] = response['email']
		oauth_token: Final[str] = response['id']
		oauth_provider: Final[str] = 'github'

		user: User = User.get_by_email(email)
		if user.oauth_provider != oauth_provider or user.oauth_token != oauth_token:
			user.oauth_token = oauth_token
			user.oauth_provider = oauth_provider
			user.update()

		user.set_session()
		flash('Logged in with GitHub successfully', 'success')
		return redirect(url_for('home.index')), 302

	except UserEmailNotFoundError:
		new_user: User = User(
			email=email,
			raw_password=None,
			oauth_token=oauth_token,
			oauth_provider=oauth_provider
		)
		new_user.create()
		new_user.set_session()
		flash('Signed up with GitHub successfully', 'success')
		return redirect(url_for('home.index')), 302

	except (ValueError, Exception) as e:
		flash('Authorization with GitHub failed', 'danger')
		app.logger.error(f'[ERROR] {e}')
		return redirect(url_for('login.email')), 302
