from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeviceForm(FlaskForm):
    devicename = StringField('Name', validators=[DataRequired()])
    devicetype = StringField('Type', validators=[DataRequired()])
    description = PasswordField('Description')
    submit = SubmitField('Submit')

class LogForm(FlaskForm):
    userid = IntegerField('Userid', validators=[DataRequired()])
    deviceid = IntegerField('Deviceid', validators=[DataRequired()])
    action = StringField('action',validators=[DataRequired()])
    log_level = StringField('log level',validators=[DataRequired()])
    submit = SubmitField('Submit')