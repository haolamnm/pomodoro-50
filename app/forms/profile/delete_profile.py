from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models.user import User


class DeleteProfileForm(FlaskForm):
	form_name: HiddenField = HiddenField(
		'form_name',
		default='delete_profile_form'
	)
	email: StringField = StringField(
		label='Current Email',
		validators=[
			DataRequired(message='Email is required'),
			Email(message='Email is invalid')
		]
	)
	password: PasswordField = PasswordField(
		label='Current Password',
		validators=[
			DataRequired(message='Password is required')
		]
	)
	submit: SubmitField = SubmitField(
		label='Delete Profile',
		render_kw={"class": "btn btn-danger", "style": "width: 100%;"}
	)

	def __init__(self, user: User, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.user = user

	def validate_email(self, field) -> None:
		if field.data != self.user.email:
			raise ValidationError('Email is incorrect')

	def validate_password(self, field) -> None:
		if hasattr(self, 'user') and not self.user.verify_password(field.data):
			raise ValidationError('Password is incorrect')
