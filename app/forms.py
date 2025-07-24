from sqlalchemy.orm import Session
from sqlalchemy import select
from app import db
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember_me = BooleanField(label="Remember Me")
    submit = SubmitField(label="Sign In")

class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = StringField(label="Password", validators=[DataRequired()])
    resubmit_password = StringField(label="Resubmit Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Register")

    def validate_username(self, username):
        select_stmt = select(User).where(User.username == username.data)
        user = db.session.scalar(select_stmt)
        if user:
            raise ValidationError("Username Already Exists! Please pick a new one!")

    def validate_email(self, email):
        select_stmt = select(User).where(User.email == email.data)
        user = db.session.scalar(select_stmt)
        if user:
            raise ValidationError("Email Already Exists! Please pick a new one!!!")
