from datetime import datetime


def datetime_to_string(obj: datetime) -> str:
	if isinstance(obj, datetime):
		return obj.isoformat()
	raise TypeError(f"Expected datetime object, got {type(obj)}")


def string_to_datetime(obj: str) -> datetime:
	if isinstance(obj, str):
		return datetime.fromisoformat(obj)
	raise TypeError(f"Expected string object, got {type(obj)}")
