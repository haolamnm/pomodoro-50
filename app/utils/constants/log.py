import os
from typing import Final


# Request Per Day (RPD)
MAX_RPD: Final[int] = 1500
RPD_LOG_FILE: Final[str] = os.path.join(
    os.path.dirname(
	os.path.dirname(
	os.path.dirname(os.path.abspath(__file__)))), 'logs', 'RPD.json'
)

# Request Per Minute (RPM)
MAX_RPM: Final[int] = 10
RPM_LOG_FILE: Final[str] = os.path.join(
    os.path.dirname(
	os.path.dirname(
	os.path.dirname(os.path.abspath(__file__)))), 'logs', 'RPM.json'
)

PROMPT_TEMPLATE_FILE: Final[str] = os.path.join(
    os.path.dirname(
	os.path.dirname(
	os.path.dirname(os.path.abspath(__file__)))), 'logs', 'prompt.txt'
)

SYSTEM_INSTRUCTION_FILE: Final[str] = os.path.join(
	os.path.dirname(
	os.path.dirname(
	os.path.dirname(os.path.abspath(__file__)))), 'logs', 'system_instruction.txt'
)

RESPONSE_LOG_FILE: Final[str] = os.path.join(
    os.path.dirname(
	os.path.dirname(
	os.path.dirname(os.path.abspath(__file__)))), 'logs', 'response.json'
)

MAX_REASON_LENGTH: Final[int] = 500

EMPTY_REASON: Final[str] = '<<EMPTY REASON>>'
EMPTY_REMAIN: Final[str] = '<<EMPTY REMAINING TIME>>'
EMPTY_TOTAL: Final[str] = '<<EMPTY TOTAL TIME>>'
EMPTY_TITLE: Final[str] = '<<EMPTY POMODORO TITLE>>'
