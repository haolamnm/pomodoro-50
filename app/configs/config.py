import os
from typing import Final, Optional
from redis import Redis
from functools import lru_cache
from datetime import timedelta
from app.utils.types import SessionType
from app.utils.environments import get_env


class Config:
	"""For general configuration"""

	# General configuration
	SECRET_KEY: Final[str] = get_env('SECRET_KEY')
	DEBUG: bool = False
	TESTING: bool = False

	# Database configuration
	SQLALCHEMY_DATABASE_URI: str = get_env('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False

	# Session configuration
	SESSION_TYPE: SessionType = 'redis'
	SESSION_FILE_DIR: Final[str] = os.path.join(os.getcwd(), 'flask_session')
	SESSION_PERMANENT: Final[bool] = False
	SESSION_USER_SIGNER: Final[bool] = True
	SESSION_KEY_PREFIX: Final[str] = 'session:'
	PERMANENT_SESSION_LIFETIME: Final[timedelta] = timedelta(weeks=1)

	# Redis configuration
	SESSION_REDIS: Optional[Redis] = Redis(
		host=get_env('REDIS_HOST'),
		port=int(get_env('REDIS_PORT')),
		password=get_env('REDIS_PASSWORD'),
		ssl=True
	)

	# Google OAuth configuration
	GOOGLE_CLIENT_ID: Final[str] = get_env('GOOGLE_CLIENT_ID')
	GOOGLE_CLIENT_SECRET: Final[str] = get_env('GOOGLE_CLIENT_SECRET')

	# Github OAuth configuration
	GITHUB_CLIENT_ID: Final[str] = get_env('GITHUB_CLIENT_ID')
	GITHUB_CLIENT_SECRET: Final[str] = get_env('GITHUB_CLIENT_SECRET')

	# Mail configuration
	MAIL_SERVER: Final[str] = get_env('MAIL_SERVER')
	MAIL_PORT: Final[int] = int(get_env('MAIL_PORT'))
	MAIL_USE_TLS: Final[bool] = True
	MAIL_USERNAME: Final[str] = get_env('MAIL_USERNAME')
	MAIL_PASSWORD: Final[str] = get_env('MAIL_PASSWORD')
