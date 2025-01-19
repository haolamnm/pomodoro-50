from flask import Flask
from app import create_app
from app.configs import DevConfig


app: Flask = create_app(DevConfig)


if __name__ == '__main__':
	app.run()
