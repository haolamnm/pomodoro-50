from typing import Final
from flask import Blueprint, jsonify, request, json, session
from datetime import datetime
from app.utils.constants.log import RESPONSE_LOG_FILE
from app.models import Pomodoro, User, Reason
from app.utils.types import GenericResponse, RequestResponseLog
from app.core.request import generate_response


core: Final[Blueprint] = Blueprint('core', __name__)


@core.route('/check/reason', methods=['POST'])
def check_reason() -> GenericResponse:
	if request.json is None:
		return jsonify({
			'status': 'error',
			'reason': 'No JSON data provided',
			'advice': 'Please provide a JSON object with a "reason" key'
		}), 400
	try:
		reason: str = request.json['reason']
		remain: str = request.json['remain'] # Remaining time
		total: str = request.json['total'] # Total time
		title: str = request.json['title'] # Title of the session

		# print(reason, remain, total, title)
		response: RequestResponseLog = generate_response(reason, remain, total, title)

		return jsonify(response), 200

	except Exception as e:
		return jsonify({
			'status': 'error',
			'reason': str(e),
			'advice': 'An unexpected error occurred'
		}), 500


@core.route('/add/pomodoro', methods=['POST'])
def create_pomodoro() -> GenericResponse:
	if request.json is None:
		return jsonify({
			'status': 'error',
			'reason': 'No JSON data provided',
			'advice': 'Please provide a valid JSON object'
		}), 400
	try:
		user_id: int = session['user_id']
		if not user_id:
			return jsonify({
				'status': 'error',
				'reason': 'User not found',
				'advice': 'Please log in to add a Pomodoro session'
			}), 401

		title: str = request.json['title']
		duration: int = request.json['duration'] # Duration in seconds
		start_at: datetime = datetime.fromisoformat(request.json['start_at'])
		end_at: datetime = datetime.fromisoformat(request.json['end_at'])
		is_completed: bool = request.json['is_completed']
		reason: str = request.json['reason']

		if not duration or duration <= 0:
			return jsonify({
				'status': 'error',
				'reason': 'Invalid duration',
				'advice': 'Please provide a valid duration in seconds'
			}), 400

		pomodoro: Pomodoro = Pomodoro(
			user_id=user_id,
			title=title,
			duration=duration,
			start_at=start_at,
			end_at=end_at,
			is_completed=is_completed,
			reason=reason
		)
		pomodoro.create()
		user: User = User.get_by_id(user_id)
		user.update_pomodoro_stats(duration, is_completed)

		return jsonify({
			'status': 'success',
			'reason': 'Pomodoro session added successfully',
			'advice': 'You can view your statistics in the dashboard'
		}), 200

	except Exception as e:
		return jsonify({
			'status': 'error',
			'reason': str(e),
			'advice': 'An unexpected error occurred'
		}), 500


@core.route('/add/invalid-reason', methods=['POST'])
def add_reason() -> GenericResponse:
	if request.json is None:
		return jsonify({
			'status': 'error',
			'reason': 'No JSON data provided',
			'advice': 'Please provide a valid JSON object'
		}), 400

	try:
		user_id: int = session['user_id']
		if not user_id:
			return jsonify({
				'status': 'error',
				'reason': 'User not found',
				'advice': 'Please log in to add a reason'
			}), 401

		ai_reason: str = request.json['reason']

		if not ai_reason:
			return jsonify({
				'status': 'error',
				'reason': 'Invalid reason',
				'advice': 'Please provide a valid reason'
			}), 400

		reason: Reason = Reason(
			user_id=user_id,
			reason=ai_reason
		)
		reason.create()

		return jsonify({
			'status': 'success',
			'reason': 'Reason added successfully',
			'advice': 'You can view your reasons in the dashboard'
		}), 200

	except Exception as e:
		return jsonify({
			'status': 'error',
			'reason': str(e),
			'advice': 'An unexpected error occurred'
		}), 500
