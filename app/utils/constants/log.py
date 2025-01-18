import os
from typing import Final


# Request Per Day (RPD)
MAX_RPD: Final[int] = 1500
RPD_LOG_FILE: Final[str] = os.path.join(
	os.path.dirname(os.path.dirname(__file__)), 'app', 'logs', 'RPD.json'
)

# Request Per Minute (RPM)
MAX_RPM: Final[int] = 10
RPM_LOG_FILE: Final[str] = os.path.join(
	os.path.dirname(os.path.dirname(__file__)), 'app', 'logs', 'RPM.json'
)

PROMPT_TEMPLATE_FILE: Final[str] = os.path.join(
	os.path.dirname(os.path.dirname(__file__)), 'app', 'logs', 'prompt.txt'
)

RESPONSE_LOG_FILE: Final[str] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'logs', 'response.json')

MAX_REASON_LENGTH: Final[int] = 500

EMPTY_REASON: Final[str] = '<<EMPTY REASON>>'
