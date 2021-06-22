# base packages

# PyPi packages
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField  # needed?
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

# custom methods and classes
from models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=15)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=60)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        """
        Checks DB to see if username has been taken.
        """
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValueError("Username already exists. Please choose another.")

    def validate_email(self, email):
        """
        Checks DB to see if email already exists.
        """
        user_email = User.query.filter_by(email=email.data).first()

        if user_email:
            raise ValueError("This email already has an account. Maybe you would like to sign in instead?")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=15)
    ])

    submit = SubmitField('Update')

    def validate_username(self, username):
        """
        Checks DB to see if username already exists
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValueError('Username already exists. Pleaes choose another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            proposed_email = User.query.filter_by(email=email.data).first()

            if proposed_email:
                raise ValueError('This email already has an account. Maybe you would like to sign in instead?')


class CreateGiftForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=1, max=100)
    ])
    link = StringField('Link', validators=[
        Length(max=100)
    ])
    description = StringField('Description', validators=[
        Length(max=140)
    ])
    public = BooleanField('Make Gift Public')
    submit = SubmitField('Add')
    # TODO: add ability to link holiday

# TODO: create UpdateGiftForm
# TODO: create HolidayForm
# TODO: create UpdateHolidayForm
