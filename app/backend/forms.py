from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")

class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    # We don't need this, but we have it just to look professional
    email = StringField(label="Email", validators=[DataRequired()])
    phoneNumber = StringField(label="phoneNumber", validators=[DataRequired()])
    age = IntegerField(label="age", validators=[DataRequired()])

    # We need the rest
    password = StringField(label="Password", validators=[DataRequired()])
    resubmit_password = StringField(label="resubmit_password", validators=[DataRequired()])
    submit = SubmitField(label="Register")
