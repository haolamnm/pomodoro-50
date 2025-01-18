from app.configs.config import Config


class DevConfig(Config):
	"""For local development environment"""

	# General configuration
	DEBUG: bool = True
	TESTING: bool = False

	# Session configuration
	SESSION_TYPE = 'filesystem'
