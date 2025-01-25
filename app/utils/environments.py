import os
from dotenv import load_dotenv


def get_env(key: str) -> str:
	load_dotenv()
	try:
		return os.environ[key]
	except KeyError as e:
		raise KeyError(f'{key} not found in .env file') from e


if __name__ == '__main__':
	pass
