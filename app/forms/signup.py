from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupEmailForm(FlaskForm):
	email: StringField = StringField(
		label='Email',
		validators=[
			DataRequired(message='Email is required'),
			Email(message='Email is invalid'),
			Length(
				max=255,
				message='Email must be less than 255 characters'
			)
		] # Database only supports 255 characters
	)
	password: PasswordField = PasswordField(
		label='Password',
		validators=[
			DataRequired(message='Password is required'),
			Length(
				min=8,
				max=255,
				message='Password must be between 8 and 255 characters'
			)
		]
	)
	confirm_password: PasswordField = PasswordField(
		label='Password confirmation',
		validators=[
			DataRequired(message='Password confirmation is required'),
			EqualTo(
				fieldname='password',
				message='Passwords must match'
			),
			Length(
				min=8,
				max=255,
				message='Password confirmation must be between 8 and 255 characters'
			)
		]
	)
	submit: SubmitField = SubmitField(
		label='Signup',
		render_kw={"class": "btn btn-primary", "style": "width: 100%;"}
	)
