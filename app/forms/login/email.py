from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email
from app.models import User
from app.utils.exceptions.user import UserEmailNotFoundError


class LoginEmailForm(FlaskForm):
	email: StringField = StringField(
		label='Email',
		validators=[
			DataRequired(message='Email is required'),
			Email(message='Email is invalid')
		]
	)
	password: PasswordField = PasswordField(
		label='Password',
		validators=[
			DataRequired(message='Password is required')
		]
	)
	submit: SubmitField = SubmitField(
		label='Email login',
		render_kw={"class": "btn btn-primary", "style": "width: 100%;"}
	)

	def validate_email(self, field):
		try:
			user: User = User.get_by_email(field.data)
			self.user = user
		except UserEmailNotFoundError:
			raise ValidationError('Email is not signed up')

	def validate_password(self, field):
		if hasattr(self, 'user') and not self.user.verify_password(field.data):
			raise ValidationError('Password is incorrect')
