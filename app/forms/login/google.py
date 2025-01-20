from flask_wtf import FlaskForm
from wtforms import SubmitField


class LoginGoogleForm(FlaskForm):
	submit: SubmitField = SubmitField(
		label='Google login',
		render_kw={"class": "btn btn-outline-danger", "style": "width: 100%;"}
	)
