from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models.user import User
from app.utils.exceptions.user import UserEmailNotFoundError


class UpdateEmailForm(FlaskForm):
	new_email: StringField = StringField(
		label='New Email',
		validators=[
			DataRequired(message='New Email is required'),
			Email(message='New Email is invalid'),
			Length(
				max=255,
				message='New Email must be less than 255 characters'
			)
		]
	)
	password: PasswordField = PasswordField(
		label='Current Password',
		validators=[
			DataRequired(message='Password is required')
		]
	)
	submit: SubmitField = SubmitField(
		label='Update Email',
		render_kw={"class": "btn btn-primary", "style": "width: 100%;"}
	)

	def __init__(self, user: User, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.user = user

	def validate_new_email(self, field) -> None:
		if field.data == self.user.email:
			raise ValidationError('Email is the same as the current email')

		try:
			User.get_by_email(field.data)
			raise ValidationError('Email is already signed up')
		except UserEmailNotFoundError:
			pass

	def validate_password(self, field) -> None:
		if hasattr(self, 'user') and not self.user.verify_password(field.data):
			raise ValidationError('Password is incorrect')
