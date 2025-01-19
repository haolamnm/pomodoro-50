from typing import Final, Optional, Self
from flask import session
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.extensions import db
from app.utils.exceptions.user import UserEmailNotFoundError, UserIdNotFoundError


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

	def set_session(self) -> None:
		"""Set the session for the user"""
		session['user_id'] = self.id
		session['email'] = self.email

	# def set_token() -> None:
	# def verify_token(token: str) -> bool:

	def set_password(self, password: str) -> None:
		self.password = generate_password_hash(password)

	def verify_password(self, password: str) -> bool:
		"""Check the password against the stored hash"""
		if isinstance(self.password, str):
			return check_password_hash(self.password, password)
		return False

	@classmethod
	def get_by_email(cls, email: str) -> Self:
		try:
			user = cls.query.filter_by(email=email).first()
			if user is None:
				raise UserEmailNotFoundError(email)
			return user
		except SQLAlchemyError as e:
			raise UserEmailNotFoundError(email) from e

	@classmethod
	def get_by_id(cls, user_id: int) -> Self:
		try:
			user = cls.query.get(user_id)
			if user is None:
				raise UserIdNotFoundError(user_id)
			return user
		except SQLAlchemyError as e:
			raise UserIdNotFoundError(user_id) from e
