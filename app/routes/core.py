import os
import sys
import subprocess
from typing import Final
from flask import Blueprint, jsonify, request, json, session
from datetime import datetime
from app.utils.constants.log import RESPONSE_LOG_FILE
from app.models import Pomodoro, User


core: Final[Blueprint] = Blueprint('core', __name__)


@core.route('/check/reason', methods=['POST'])
def check_reason():
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

		result = subprocess.run(
			[sys.executable, '-m', 'app.core.request', reason, remain, total, title],
			capture_output=True,
			text=True,
			check=True
		)
		# For debugging purposes
		# print(f"Running command: python -m app.core.request '{reason}'")
		# print(f"STDOUT: {result.stdout}")
		# print(f"STDERR: {result.stderr}")

		with open(RESPONSE_LOG_FILE, 'r') as file:
			ai_response = json.load(file)

		# TODO: Save the user's reason in the database

		return jsonify(ai_response), 200

	except subprocess.CalledProcessError as e:
		# print(f"Subprocess error: {e}")
		# print(f"STDOUT: {result.stdout}")
		# print(f"STDERR: {result.stderr}")
		return jsonify({
			'status': 'error',
			'reason': str(e),
			'advice': 'Error in running the request script'
		}), 500

	except Exception as e:
		# print(f"General error: {e}")
		return jsonify({
			'status': 'error',
			'reason': str(e),
			'advice': 'An unexpected error occurred'
		}), 500


@core.route('/add/pomodoro', methods=['POST'])
def update_pomodoro():
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
