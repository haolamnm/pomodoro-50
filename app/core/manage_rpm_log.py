import os
import json
from app.utils.converters import datetime_to_string, string_to_datetime
from app.utils.types.core import RequestsPerMinuteLog
from app.utils.constants.log import MAX_RPM, RPM_LOG_FILE
from datetime import datetime, timedelta


def save_requests_per_minute_log(data: RequestsPerMinuteLog) -> None:
	with open(RPM_LOG_FILE, 'w') as file:
		json.dump(data, file, indent=4, default=datetime_to_string)


def load_requests_per_minute_log() -> RequestsPerMinuteLog:
	if not os.path.exists(RPM_LOG_FILE):
		data: RequestsPerMinuteLog = {'timestamps': []}
		save_requests_per_minute_log(data)

	with open(RPM_LOG_FILE, 'r') as file:
		data: RequestsPerMinuteLog = json.load(file)
		timestamps: list[str] = list(map(str, data['timestamps']))
		data['timestamps'] = list(map(string_to_datetime, timestamps))
		reset_requests_per_minute_log(data)

	return data


def reset_requests_per_minute_log(data: RequestsPerMinuteLog) -> None:
	now: datetime = datetime.now()
	one_minute_ago: datetime = now - timedelta(minutes=1)

    # Filter timestamps to only include those within the last minute
	data['timestamps'] = [
	    timestamp for timestamp in data['timestamps']
	    if timestamp > one_minute_ago
    ]
	save_requests_per_minute_log(data)


def check_requests_per_minute_log(data: RequestsPerMinuteLog) -> bool:
	request_timestamps: list[datetime] = data['timestamps']

	remaning_requests: int = MAX_RPM - len(request_timestamps)
	print(f'[INFO] RPM remain: {remaning_requests - 1}/{MAX_RPM}')

	if remaning_requests > 0:
		request_timestamps.append(datetime.now())
		save_requests_per_minute_log(data)
		return True

	wait_time: float = (request_timestamps[0] + timedelta(minutes=1) - datetime.now()).total_seconds()
	print(f'[INFO] RPM limit reached. Please wait for {wait_time:.2f} seconds.')
	return False
