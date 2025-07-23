from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")

class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = StringField(label="Password", validators=[DataRequired()])
    resubmit_password = StringField(label="Resubmit Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Register")

    # This is here to remember additional functionality
    # def validate_<field_name>: This will tell WTForm to also use this to validate the user input on given <field_name>
