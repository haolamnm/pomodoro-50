import sys
from app.utils.types.core import RequestResponseLog
from app.utils.constants import *
from app.core.manage_rpd_log import *
from app.core.manage_rpm_log import *
from app.utils.extensions import gemini


def create_prompt(reason: str, remain: str, total: str, title: str) -> str:
	"""Create a prompt based on the given reason"""
	with open(PROMPT_TEMPLATE_FILE, 'r') as file:
		prompt = file.read()

	prompt = prompt.replace(EMPTY_REASON, reason)
	prompt = prompt.replace(EMPTY_REMAIN, remain)
	prompt = prompt.replace(EMPTY_TOTAL, total)
	prompt = prompt.replace(EMPTY_TITLE, title)

	return prompt


def make_request_to_gemini(prompt: str) -> str:
	response = gemini.generate_content(prompt)
	content: str = response.text

	# Update the daily request count
	data = load_requests_per_day_log()
	data['count'] += 1
	save_requests_per_day_log(data)

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

	RPD_log: RequestsPerDayLog = load_requests_per_day_log()
	if not check_requests_per_day_log(RPD_log):
		response: RequestResponseLog = {
			'status': 'valid',
			'reason': 'The daily request limit has been reached',
			'advice': 'Please try again tomorrow'
		}
		return response

	RPM_log: RequestsPerMinuteLog = load_requests_per_minute_log()
	if not check_requests_per_minute_log(RPM_log):
		response: RequestResponseLog = {
			'status': 'invalid',
			'reason': 'The minute request limit has been reached',
			'advice': 'Please try again in a minute'
		}
		return response

	prompt: str = create_prompt(reason, remain, total, title)
	raw_response: str = make_request_to_gemini(prompt)
	response: RequestResponseLog = clean_response(raw_response)

	return response


def save_response(response: RequestResponseLog) -> None:
	with open(RESPONSE_LOG_FILE, 'w') as file:
		json.dump(response, file, indent=4)


def main(reason: str, remain: str, total: str, title: str) -> None:
	response: RequestResponseLog = generate_response(reason, remain, total, title)
	save_response(response)


if __name__ == '__main__':
	# Take 4 arguments: reason, remain, total, title
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
