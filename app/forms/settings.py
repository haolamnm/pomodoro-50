from flask_wtf import FlaskForm
from wtforms.fields import SelectField, SubmitField
from wtforms.validators import DataRequired


class DurationSettingsForm(FlaskForm):
	duration: SelectField = SelectField(
		label='Session Duration',
		choices=[
			('25:00', '25 minutes'),
			('35:00', '35 minutes'),
			('50:00', '50 minutes'),
			('60:00', '60 minutes')
		],
		default='25:00',
		validators=[
			DataRequired(message='Selcecting a duration is required')
		]
	)
	submit: SubmitField = SubmitField(
		label='Save',
		render_kw={"class": "btn btn-primary", "style": "width: 100%;"}
	)
