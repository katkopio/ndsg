from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange#, Length, Email, EqualTo, ValidationError
# from wtforms import PasswordField, BooleanField, TextAreaField, DateField

class InputGPXFileForm(FlaskForm):
    gpx_file = FileField('GPX File', validators=[FileAllowed(['gpx']), DataRequired()])
    submit = SubmitField('Calculate')

class SpeedViolationForm(FlaskForm):
    gpx_file = FileField('GPX File', validators=[FileAllowed(['gpx']), DataRequired()])
    speed_limit = FloatField('Speed Limit (in kph)', validators=[NumberRange(), DataRequired()])
    time_minutes = FloatField('Duration (in minutes)', validators=[NumberRange(), DataRequired()])
    analysis_type = SelectField('Analysis Type', choices=[('exp', 'Explicit'), ('loc', 'Location')], validators=[DataRequired()])
    submit = SubmitField('Calculate')

class GeofencingForm(FlaskForm):
    gpx_file = FileField('GPX File', validators=[FileAllowed(['gpx']), DataRequired()])
    submit = SubmitField('See Points')
    lat1 = StringField('Latitude 1')
    lon1 = StringField('Longitude 1')
    lon2 = StringField('Longitude 2')
    lat2 = StringField('Latitude 2')
    min_time = StringField('Minimum Time (seconds)')
    max_time = StringField('Maximum Time (seconds)')
    compute = SubmitField('Compute')

class LivenessForm(FlaskForm):
    gpx_file = FileField('GPX File', validators=[FileAllowed(['gpx']), DataRequired()])
    time_limit = FloatField('Time Limit (in seconds)', validators=[NumberRange(), DataRequired()])
    submit = SubmitField('Calculate')

# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')

#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('That username is taken. Please choose a different one.')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please choose a different one.')