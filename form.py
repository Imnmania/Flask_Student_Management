from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo


class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class RegisterForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    submit = SubmitField('Register')