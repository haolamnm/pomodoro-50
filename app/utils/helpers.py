from datetime import datetime


def get_weekly_duration(durations: list[int], start_ats: list[datetime]) -> list[float]:
	weekly_durations: list[float] = [0, 0, 0, 0, 0, 0, 0]

	for duration, start_at in zip(durations, start_ats):
		day_index = start_at.weekday()
		weekly_durations[day_index] += duration

	# Convert seconds to minutes
	# Round to 2 decimal places
	weekly_durations = [round(duration / 60, 2) for duration in weekly_durations]

	return weekly_durations

