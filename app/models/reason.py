from typing import Final
from datetime import datetime
from app.utils.extensions import db

class Reason(db.Model):
	__tablename__: Final[str] = 'reasons'

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
	reason: str = db.Column(
		db.String(255),
		nullable=False,
		unique=False
	)
	create_at: datetime = db.Column(
		db.DateTime,
		nullable=False,
		unique=False,
		server_default=db.func.now()
	)

	def __init__(self, user_id: int, reason: str) -> None:
		self.user_id = user_id
		self.reason = reason

	def create(self) -> None:
		db.session.add(self)
		db.session.commit()
