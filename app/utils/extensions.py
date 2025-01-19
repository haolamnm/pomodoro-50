import logging
from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai
from google.generativeai import GenerativeModel
from authlib.integrations.flask_client import OAuth
from app.utils.environments import get_env


genai.configure(
	api_key=get_env('GOOGLE_API_KEY')
)
gemini: GenerativeModel = genai.GenerativeModel(
	model_name='gemini-2.0-flash-exp'
)


db: SQLAlchemy = SQLAlchemy()
mail: Mail = Mail()
oauth: OAuth = OAuth()
session: Session = Session()
migrate: Migrate = Migrate()
stream_handler = logging.StreamHandler()


def init_extensions(app: Flask) -> None:
	db.init_app(app)
	mail.init_app(app)
	oauth.init_app(app)
	session.init_app(app)
	migrate.init_app(app, db)
	stream_handler.setLevel(logging.INFO)
	app.logger.addHandler(stream_handler)
	app.logger.setLevel(logging.INFO)


def init_google(app: Flask) -> None:
	oauth.register(
		name='google',
		client_id=app.config['GOOGLE_CLIENT_ID'],
		client_secret=app.config['GOOGLE_CLIENT_SECRET'],
		server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
		client_kwargs={
			'scope': 'openid email profile'
    	}
	)


def init_github(app: Flask) -> None:
	oauth.register(
		name='github',
		client_id=app.config['GITHUB_CLIENT_ID'],
		client_secret=app.config['GITHUB_CLIENT_SECRET'],
		access_token_url='https://github.com/login/oauth/access_token',
		access_token_params=None,
		authorize_url='https://github.com/login/oauth/authorize',
		authorize_params=None,
		api_base_url='https://api.github.com/',
		client_kwargs={
			'scope': 'user:email'
		}
	)
