from app.configs.config import Config


class TestConfig(Config):
	"""For running tests"""

	# General configuration
	DEBUG: bool = False
	TESTING: bool = True

	# Session configuration
	SESSION_TYPE = 'filesystem'
	SESSION_REDIS = None

	# Database configuration
	SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'
