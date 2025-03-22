from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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