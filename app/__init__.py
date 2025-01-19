from typing import Type
from flask import Flask, jsonify, url_for
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
from app.utils.types import RouteResponse


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

	return app


def init_error_handlers(app: Flask) -> None:
	@app.errorhandler(404)
	def handle_404_error(error) -> RouteResponse:
		return jsonify({
			'message': 'Page not found.',
			'category': 'danger',
			'redirect': url_for('home.index')
		}), 404

	@app.errorhandler(500)
	def handle_500_error(error) -> RouteResponse:
		"""Handle 500 Internal Server Error"""
		return jsonify({
			'message': 'Server error.',
			'category': 'danger',
			'redirect': url_for('home.index')
		}), 500
