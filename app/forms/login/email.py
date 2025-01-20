from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models.user import User
from app.utils.exceptions.user import UserEmailNotFoundError


class LoginEmailForm(FlaskForm):
	form_name: HiddenField = HiddenField(
		'form_name',
		default='login_email_form'
	)
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
		label='Login',
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
