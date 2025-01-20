from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, HiddenField


class LoginGoogleForm(FlaskForm):
	form_name: HiddenField = HiddenField(
		'form_name',
		default='login_google_form'
	)
	submit: SubmitField = SubmitField(
		label='Google',
		render_kw={"class": "btn btn-outline-danger", "style": "width: 100%;"}
	)
