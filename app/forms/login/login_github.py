from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, HiddenField


class LoginGitHubForm(FlaskForm):
	form_name: HiddenField = HiddenField(
		'form_name',
		default='login_github_form'
	)
	submit: SubmitField = SubmitField(
		label='GitHub',
		render_kw={"class": "btn btn-outline-light", "style": "width: 100%;"}
	)
