from app.configs.config import Config


class DevConfig(Config):
	"""For local development environment"""

	# General configuration
	_DEBUG = True
	_TESTING = False

	# Session configuration
	_SESSION_TYPE = 'filesystem'
	_SESSION_REDIS = None
