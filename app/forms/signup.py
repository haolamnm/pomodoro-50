from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(FlaskForm):
	email: StringField = StringField(
		label='Email',
		validators=[
			DataRequired(),
			Email(),
			Length(max=255)
		] # Database only supports 255 characters
	)
	password: PasswordField = PasswordField(
		label='Password',
		validators=[
			DataRequired(),
			Length(min=8, max=255)
		]
	)
	confirm_password: PasswordField = PasswordField(
		label='Password confirmation',
		validators=[
			DataRequired(),
			EqualTo(
				fieldname='password',
				message='Passwords must match.'
			),
			Length(min=8, max=255)
		]
	)
	submit: SubmitField = SubmitField(
		label='Signup',
		render_kw={"class": "btn btn-primary", "style": "width: 100%;"}
	)
