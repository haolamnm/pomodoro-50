from typing import Final
from redis import Redis
from datetime import timedelta
from app.utils.types import SessionType
from app.utils.environments import get_env


class Config:
	# General configuration
	__SECRET_KEY: Final[str] = get_env('SECRET_KEY')
	_DEBUG: bool = False
	_TESTING: bool = False

	# Database configuration
	__SQLALCHEMY_DATABASE_URI: Final[str] = get_env('SQLALCHEMY_DATABASE_URI')
	__SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False

	# Session configuration
	_SESSION_TYPE: SessionType = 'redis'
	_SESSION_REDIS: Final[Redis] = Redis(
		host=get_env('REDIS_HOST'),
		port=int(get_env('REDIS_PORT')),
		password=get_env('REDIS_PASSWORD'),
		ssl=True
	)
	__SESSION_PERMANENT: Final[bool] = False
	__SESSION_USER_SIGNER: Final[bool] = True
	__SESSION_KEY_PREFIX: Final[str] = 'session:'
	__PERMANENT_SESSION_LIFETIME: Final[timedelta] = timedelta(weeks=1)

	# Google OAuth configuration
	__GOOGLE_CLIENT_ID: Final[str] = get_env('GOOGLE_CLIENT_ID')
	__GOOGLE_CLIENT_SECRET: Final[str] = get_env('GOOGLE_CLIENT_SECRET')

	# Github OAuth configuration
	__GITHUB_CLIENT_ID: Final[str] = get_env('GITHUB_CLIENT_ID')
	__GITHUB_CLIENT_SECRET: Final[str] = get_env('GITHUB_CLIENT_SECRET')

	# Mail configuration
	__MAIL_SERVER: Final[str] = get_env('MAIL_SERVER')
	__MAIL_PORT: Final[int] = int(get_env('MAIL_PORT'))
	__MAIL_USE_TLS: Final[bool] = True
	__MAIL_USERNAME: Final[str] = get_env('MAIL_USERNAME')
	__MAIL_PASSWORD: Final[str] = get_env('MAIL_PASSWORD')
