from flask_wtf import FlaskForm
from wtforms import SubmitField


class LoginGitHubForm(FlaskForm):
	submit: SubmitField = SubmitField(
		label='GitHub login',
		render_kw={"class": "btn btn-outline-light", "style": "width: 100%;"}
	)
