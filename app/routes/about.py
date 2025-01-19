from typing import Final
from flask import Blueprint, render_template
from app.utils.decorators import login_required


about: Final[Blueprint] = Blueprint('about', __name__)


@about.route('/', methods=['GET'])
@login_required
def index() -> str:
	return render_template('about/index.html')
