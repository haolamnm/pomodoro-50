import os
import sys
import subprocess
from typing import Final
from flask import Blueprint, jsonify, request, json
from app.utils.constants.log import RESPONSE_LOG_FILE


core: Final[Blueprint] = Blueprint('core', __name__)


@core.route('/check-reason', methods=['POST'])
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
