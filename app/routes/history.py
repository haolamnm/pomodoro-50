from typing import Final
from flask import Blueprint, render_template
from app.utils.decorators import login_required


history: Final[Blueprint] = Blueprint('history', __name__)


@history.route('/', methods=['GET'])
@login_required
def index() -> str:
	return render_template('history/index.html')
