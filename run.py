from flask import Flask
from app import create_app
from app.configs.config import Config


app: Flask = create_app(Config)


if __name__ == '__main__':
	app.run()
