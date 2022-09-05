from datetime import datetime as d
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError, Regexp
import email_validator
from ..models import User, Role


class LoginForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('')


class RegisterForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired(), validators.Length(min=5, max=35), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames can only have letters, numbers, underscores or dots')])
    email = StringField('Enter Email address', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('Enter Password', validators=[InputRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=32), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('')

    # validate that username does not already exist. N/B- username_to_check can be any variable at all
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    # validate that email does not already exist
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email is already registered! Please try a different email address')