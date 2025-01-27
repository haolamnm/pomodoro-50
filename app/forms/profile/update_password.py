from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.user import User


class UpdatePasswordForm(FlaskForm):
	new_password: PasswordField = PasswordField(
		label='New Password',
		validators=[
			DataRequired(message='New Password is required'),
			Length(
				min=8,
				max=255,
				message='New Password must be between 8 and 255 characters'
			)
		]
	)
	password: PasswordField = PasswordField(
		label='Current Password',
		validators=[
			DataRequired(message='Current Password is required')
		]
	)
	submit: SubmitField = SubmitField(
		label='Update Password',
		render_kw={"class": "btn btn-primary", "style": "width: 100%;"}
	)

	def __init__(self, user: User, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.user = user

	def validate_password(self, field) -> None:
		if hasattr(self, 'user') and self.user.password is None:
			raise ValidationError('Since you signed up with Google or GitHub account, you need to go to "forgot password" to set a password')

		if not self.user.verify_password(field.data):
			raise ValidationError('Password is incorrect')

		if self.new_password.data == field.data:
			raise ValidationError('Password is the same as the current password')
