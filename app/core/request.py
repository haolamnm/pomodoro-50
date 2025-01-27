import json
from app.utils.types.core import RequestResponseLog
from app.utils.constants import *
# from app.core.manage_rpd_log import *
# from app.core.manage_rpm_log import *
from app.utils.extensions import gemini


def create_prompt(reason: str, remain: str, total: str, title: str) -> str:
	"""Create a prompt based on the given reason"""
	prompt: str = f'''A user stopped a Pomodoro session with the following details:
reason: {reason}
remaining time of that session: {remain[0:2]} minutes and {remain[3:5]} seconds
total time of that session: {total[0:2]} minutes and {total[3:5]} seconds
the user is working with: {title}
	'''

	return prompt


def make_request_to_gemini(prompt: str) -> str:
	response = gemini.generate_content(prompt)
	content: str = response.text

	# Update the daily request count
	# data = load_requests_per_day_log()
	# data['count'] += 1
	# save_requests_per_day_log(data)

	return content


def clean_response(raw_response: str) -> RequestResponseLog:
	response: str = raw_response.strip().replace('json\n', '').strip().replace('```', '')
	try:
		cleaned_response: RequestResponseLog = json.loads(response)
	except json.JSONDecodeError:
		cleaned_response: RequestResponseLog = {
			'status': 'valid',
			'reason': 'An error occurred while cleaning the response',
			'advice': 'Hi there! I am PomoPal, looks like I am having a bad day. For now, you can stop the timer. Please try again next time!'
		}
	return cleaned_response


def generate_response(reason: str, remain: str, total: str, title: str) -> RequestResponseLog:
	"""Generate a response based on the given reason"""
	if len(reason) > MAX_REASON_LENGTH:
		response: RequestResponseLog = {
			'status': 'invalid',
			'reason': 'The reason is too long',
			'advice': 'Please provide a reason that is less than 500 characters'
		}
		return response

	# RPD_log: RequestsPerDayLog = load_requests_per_day_log()
	# if not check_requests_per_day_log(RPD_log):
	# 	response: RequestResponseLog = {
	# 		'status': 'valid',
	# 		'reason': 'The daily request limit has been reached',
	# 		'advice': 'Please try again tomorrow'
	# 	}
	# 	return response

	# RPM_log: RequestsPerMinuteLog = load_requests_per_minute_log()
	# if not check_requests_per_minute_log(RPM_log):
	# 	response: RequestResponseLog = {
	# 		'status': 'invalid',
	# 		'reason': 'The minute request limit has been reached',
	# 		'advice': 'Please try again in a minute'
	# 	}
	# 	return response

	prompt: str = create_prompt(reason, remain, total, title)
	raw_response: str = make_request_to_gemini(prompt)
	response: RequestResponseLog = clean_response(raw_response)

	return response


if __name__ == '__main__':
	pass
