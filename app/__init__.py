from typing import Type
from flask import Flask
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


def create_app(config_class: Type[Config]) -> Flask:
	app: Flask = Flask(__name__)
	app.config.from_object(config_class)

	init_extensions(app)
	init_github(app)
	init_google(app)

	with app.app_context():
		db.create_all()

	init_routes(app)

	# TODO: Add error handling

	return app
