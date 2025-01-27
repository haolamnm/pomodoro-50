from typing import Final
from flask import Blueprint, render_template
from app.utils.decorators import login_required
from app.utils.types import RenderResponse


about: Final[Blueprint] = Blueprint('about', __name__)


@about.route('/', methods=['GET'])
@about.route('/app', methods=['GET'])
@login_required
def app() -> RenderResponse:
	return render_template('about.html'), 200
