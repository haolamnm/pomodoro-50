from typing import Final, Literal
from datetime import datetime
from app.utils.extensions import db


class Pomodoro(db.Model):
	__tablename__: Final[str] = 'pomodoros'

	id: int = db.Column(
		db.Integer,
		primary_key=True,
		autoincrement=True,
		nullable=False,
		unique=True
	)
	user_id: int = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False,
		unique=False
	)
	title: str = db.Column(
		db.String(255),
		nullable=False,
		unique=False
	)
	duration: int = db.Column(
		db.Integer,
		nullable=False,
		unique=False
	)
	start_at: datetime = db.Column(
		db.DateTime,
		nullable=False,
		unique=False,
		server_default=db.func.now()
	)
	end_at: datetime = db.Column(
		db.DateTime,
		nullable=True,
		unique=False
	)
	is_completed: bool = db.Column(
		db.Boolean,
		nullable=False,
		unique=False,
		server_default='0'
	)
	reason: str = db.Column(
		db.String(255),
		nullable=True,
		unique=False
	)

	def __init__(self, user_id: int, title: str, duration: int, start_at: datetime, end_at: datetime, is_completed: bool, reason: str) -> None:
		self.user_id = user_id
		self.title = title
		self.duration = duration
		self.start_at = start_at
		self.end_at = end_at
		self.is_completed = is_completed
		self.reason = reason

	def create(self) -> None:
		db.session.add(self)
		db.session.commit()

	@classmethod
	def get_by_user_id(cls, user_id: int, type: Literal['asc', 'desc'] = 'asc') -> list['Pomodoro']:
		try:
			if type == 'asc':
				return cls.query.filter_by(user_id=user_id).all()
			elif type == 'desc':
				return cls.query.filter_by(user_id=user_id).order_by(db.desc(cls.start_at)).all()
			else:
				raise Exception('Invalid type')
		except Exception as e:
			return []

	@classmethod
	def get_by_time(cls, user_id: int, start_at: datetime, end_at: datetime) -> list['Pomodoro']:
		try:
			return cls.query.filter(
				db.and_(
					cls.user_id == user_id,
					cls.start_at >= start_at,
					cls.start_at <= end_at
				)
			).all()
		except Exception:
			return []
