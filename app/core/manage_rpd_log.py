import os
import json
from app.utils.types.core import RequestsPerDayLog
from app.utils.constants.log import MAX_RPD, RPD_LOG_FILE
from datetime import datetime


def save_requests_per_day_log(data: RequestsPerDayLog) -> None:
	with open(RPD_LOG_FILE, 'w') as file:
		json.dump(data, file, indent=4)


def load_requests_per_day_log() -> RequestsPerDayLog:
	if not os.path.exists(RPD_LOG_FILE):
		data: RequestsPerDayLog = {'date': str(datetime.now().date()), 'count': 0}
		save_requests_per_day_log(data)

	with open(RPD_LOG_FILE, 'r') as file:
		data: RequestsPerDayLog = json.load(file)
		reset_requests_per_day_log(data)

	return data


def reset_requests_per_day_log(data: RequestsPerDayLog) -> None:
	current_date: str = str(datetime.now().date())

	if data['date'] != current_date:
		data['date'] = current_date
		data['count'] = 0
		save_requests_per_day_log(data)


def check_requests_per_day_log(data: RequestsPerDayLog) -> bool:
	if data['count'] >= MAX_RPD:
		print(f'[INFO] RPD limit reached. Please wait until tomorrow.')
		# app.logger.info
		return False

	return True
