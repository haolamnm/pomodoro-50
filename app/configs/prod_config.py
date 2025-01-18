from app.configs.config import Config


class ProdConfig(Config):
	"""For production configuration"""

	# General configuration
	DEBUG: bool = False
	TESTING: bool = False
