from typing import Type
from flask import Flask, Response, url_for, flash, redirect
from app.configs import Config
from app.utils.extensions import (
	db,
	init_extensions,
	init_github,
	init_google,
)
from app.routes import (
	init_routes,
)
from app.utils.types.route import RedirectResponse


def create_app(config_class: Type[Config]) -> Flask:
	app: Flask = Flask(__name__)
	app.config.from_object(config_class)

	init_extensions(app)
	init_github(app)
	init_google(app)

	with app.app_context():
		db.create_all()

	init_routes(app)
	init_error_handlers(app)
	init_after_request(app)

	return app


def init_error_handlers(app: Flask) -> None:
	@app.errorhandler(404)
	def handle_404_error(error) -> RedirectResponse:
		flash('Page not found', 'info')
		return redirect(url_for('home.index')), 301

	@app.errorhandler(500)
	def handle_500_error(error) -> RedirectResponse:
		"""Handle 500 Internal Server Error"""
		flash('Internal server error', 'danger')
		return redirect(url_for('home.index')), 301


def init_after_request(app: Flask) -> None:
	@app.after_request
	def after_request(response: Response) -> Response:
		""""This function ensures responses aren't cached."""
		response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
		response.headers['Expires'] = 0
		response.headers['Pragma'] = 'no-cache'
		return response
