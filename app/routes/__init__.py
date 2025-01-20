from flask import Flask

from app.routes.core import core
from app.routes.home import home
from app.routes.about import about
from app.routes.login import login
from app.routes.logout import logout
from app.routes.signup import signup
from app.routes.history import history
from app.routes.profile import profile
from app.routes.insights import insights
from app.routes.settings import settings


def init_routes(app: Flask) -> None:
	app.register_blueprint(home, url_prefix='/')
	app.register_blueprint(core, url_prefix='/core')
	app.register_blueprint(about, url_prefix='/about')
	app.register_blueprint(login, url_prefix='/login')
	app.register_blueprint(logout, url_prefix='/logout')
	app.register_blueprint(signup, url_prefix='/signup')
	app.register_blueprint(history, url_prefix='/history')
	app.register_blueprint(profile, url_prefix='/profile')
	app.register_blueprint(insights, url_prefix='/insights')
	app.register_blueprint(settings, url_prefix='/settings')
