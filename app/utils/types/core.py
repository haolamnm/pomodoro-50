from typing import TypedDict, Literal
from datetime import datetime


class RequestsPerDayLog(TypedDict):
	date: str
	count: int


class RequestsPerMinuteLog(TypedDict):
	timestamps: list[datetime]


class RequestResponseLog(TypedDict):
	status: Literal['valid', 'invalid']
	reason: str
	advice: str
