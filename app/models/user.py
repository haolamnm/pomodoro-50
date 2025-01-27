from typing import Final, Optional, Self
from flask import url_for, render_template, session
from flask_mail import Message
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from app.utils.environments import get_env
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
		server_default='0' # in seconds
	)
	custom_pomodoro_time: str = db.Column(
		db.String(5),
		nullable=False,
		unique=False,
		server_default='50:00'
	)

	pomodoros = db.relationship('Pomodoro', backref='user', lazy=True)
	reasons = db.relationship('Reason', backref='user', lazy=True)

	def __init__(self, email: str, raw_password: Optional[str], **kwargs) -> None:
		self.email = email
		if raw_password:
			self.set_password(raw_password)
		for key, value in kwargs.items():
			setattr(self, key, value)

	def create(self) -> None:
		"""Create the user in the database"""
		db.session.add(self)
		db.session.commit()

	def update(self) -> None:
		"""Update the user in the database"""
		db.session.commit()

	def update_pomodoro_stats(self, duration: int, is_completed: bool) -> None:
		try:
			self.total_pomodoros_completed += 1 if is_completed else 0
			self.total_time_spent += duration
			self.update()
		except Exception as e:
			db.session.rollback()
			raise RuntimeError('Error in updating user stats') from e

	def update_custom_pomodoro_time(self, custom_pomodoro_time: str) -> None:
		self.custom_pomodoro_time = custom_pomodoro_time
		self.update()

	def delete(self) -> None:
		"""Delete the user from the database"""
		db.session.delete(self)
		db.session.commit()

	def set_session(self) -> None:
		"""Set the session for the user"""
		session['user_id'] = self.id
		session['user_email'] = self.email

	def set_last_login_at(self) -> None:
		"""Set the last login time"""
		self.last_login_at = datetime.now()
		self.update()

	def set_token(self) -> str:
		serializer: Serializer = Serializer(get_env('SECRET_KEY'))
		data: dict[str, int] = {'user_id': self.id}
		token: str = serializer.dumps(data)
		return token

	@staticmethod
	def verify_token(token: str) -> 'User':
		serializer: Serializer = Serializer(get_env('SECRET_KEY'))
		try:
			data: dict[str, int] = serializer.loads(token)
			if not 'user_id' in data:
				raise KeyError('User ID not found in token')
			user_id: int = data['user_id']
			user: 'User' = User.get_by_id(user_id)
			return user
		except (KeyError, UserIdNotFoundError, Exception) as e:
			raise ValueError('Token is invalid') from e

	def set_password(self, raw_password: str) -> None:
		"""Set the password hash"""
		self.password = generate_password_hash(raw_password)

	def verify_password(self, password: str) -> bool:
		"""Check the password against the stored hash"""
		if isinstance(self.password, str):
			return check_password_hash(self.password, password)
		return False

	def create_reset_password_email(self) -> Message:
		"""Create the reset password email"""
		token: str = self.set_token()
		msg: Message = Message(
			subject='[Pomodoro 50] Reset Password Request',
			sender=get_env('MAIL_USERNAME'),
			recipients=[self.email]
		)
		reset_password_url: str = url_for(
			'profile.reset_password_token',
			token=token,
			_external=True
		)
		msg.body = render_template(
			'emails/reset_password_email.txt',
			email=self.email,
			reset_password_url=reset_password_url
		)
		msg.html = render_template(
			'emails/reset_password_email.html',
			email=self.email,
			reset_password_url=reset_password_url
		)

		return msg

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
