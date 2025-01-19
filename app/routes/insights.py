from typing import Final
from flask import Blueprint, render_template
from app.utils.decorators import login_required


insights: Final[Blueprint] = Blueprint('insights', __name__)


@insights.route('/', methods=['GET'])
@login_required
def index() -> str:
	return render_template('insights/index.html')
