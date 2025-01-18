from typing import Final, Optional
from datetime import datetime
from app.utils.extensions import db


class User(db.Model):
	__tablename__: Final[str] = 'users'

	id: int = db.Column(
		db.Integer,
		primary_key=True,
		autoincrement=True,
		nullable=False,
		unique=True
	)
	email: str = db.Column(
		db.String(255),
		nullable=False,
		unique=True
	)
	password: Optional[str] = db.Column(
		db.String(255),
		nullable=True,
		unique=False
	)
	create_at: datetime = db.Column(
		db.DateTime,
		nullable=False,
		unique=False,
		server_default=db.func.now()
		# default=datetime.now(timezone.utc)
	)
	oauth_provider: Optional[str] = db.Column(
		db.String(255),
		nullable=True,
		unique=False
	)
	oauth_token: Optional[str] = db.Column(
		db.String(255),
		nullable=True,
		unique=False
	)
	last_login_at: datetime = db.Column(
		db.DateTime,
		nullable=False,
		unique=False,
		server_default=db.func.now()
	)
	total_pomodoros_completed: int = db.Column(
		db.Integer,
		nullable=False,
		unique=False,
		server_default='0'
	)
	total_time_spent: int = db.Column(
		db.Integer,
		nullable=False,
		unique=False,
		server_default='0'
	)
	custom_pomodoro_time: int = db.Column(
		db.Integer,
		nullable=False,
		unique=False,
		server_default='50'
	)
	custom_short_break_time: int = db.Column(
		db.Integer,
		nullable=False,
		unique=False,
		server_default='10'
	)
	custom_long_break_time: int = db.Column(
		db.Integer,
		nullable=False,
		unique=False,
		server_default='30'
	)

	pomodoros = db.relationship('Pomodoro', backref='user', lazy=True)
