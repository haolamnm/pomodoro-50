from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginEmailForm(FlaskForm):
	email: StringField = StringField(
		label='Email',
		validators=[DataRequired(), Email()]
	)
	password: PasswordField = PasswordField(
		label='Password',
		validators=[DataRequired()]
	)
	submit: SubmitField = SubmitField(
		label='Email login',
		render_kw={"class": "btn btn-primary", "style": "width: 100%;"}
	)
