from datetime import datetime
from app.models import Pomodoro
from app.utils.types import DurationLog


def get_weekly_duration(durations: list[int], start_ats: list[datetime]) -> list[float]:
	weekly_durations: list[float] = [0, 0, 0, 0, 0, 0, 0]

	for duration, start_at in zip(durations, start_ats):
		day_index = start_at.weekday()
		weekly_durations[day_index] += duration

	# Convert seconds to minutes
	# Round to 2 decimal places
	weekly_durations = [round(duration / 60, 2) for duration in weekly_durations]

	return weekly_durations


def get_all_time_duration(pomodoros: list[Pomodoro]) -> list[DurationLog]:
	date_duration_logs: dict[str, float] = {}

	for pomodoro in pomodoros:
		date: str = pomodoro.start_at.strftime('%Y-%m-%d')
		duration: float = round(pomodoro.duration / 60, 2) # Convert seconds to minutes
		date_duration_logs[date] = date_duration_logs.get(date, 0) + duration

	all_time_duration_logs: list[DurationLog] = [
		{'date': date, 'value': duration}
		for date, duration in date_duration_logs.items()
	]

	return all_time_duration_logs
