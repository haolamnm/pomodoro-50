from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models.user import User
from app.utils.exceptions.user import UserEmailNotFoundError


class ResetPasswordRequestForm(FlaskForm):
	email: StringField = StringField(
		label='Email',
		validators=[
			DataRequired(message='Email is required'),
			Email(message='Email is invalid')
		]
	)
	submit: SubmitField = SubmitField(
		label='Send Reset Email',
		render_kw={"class": "btn btn-primary", "style": "width: 100%;"}
	)

	def validate_email(self, field):
		try:
			user: User = User.get_by_email(field.data)
			self.user = user
		except UserEmailNotFoundError:
			raise ValidationError('Email is not signed up')
