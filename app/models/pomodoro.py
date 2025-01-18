from typing import Final, Optional
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
	end_at: Optional[datetime] = db.Column(
		db.DateTime,
		nullable=True,
		unique=False
	) # If the Pomodoro is completed, this field will be updated

	@property
	def is_completed(self) -> bool:
		return self.end_at is not None
