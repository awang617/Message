from flask_wtf import FlaskForm as Form

from models import User

from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Regexp, ValidationError, Length, EqualTo, Email


def name_exists(form, field):
    # if the user already exists
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with this username already exists!")


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Someone with this email is already signed up!")


class RegisterForm(Form):
    fname = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z_]+$',
                message=(
                    "Cannot contain numbers or special characters"
                )
        ]
    )
    fname = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z_]+$',
                message=(
                    "Cannot contain numbers or special characters"
                )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )

class Account(Form):
    email = StringField(
        'Email', 
        validators=[DataRequired(), 
        Email()]
        )


class LoginForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])

class ReviewForm(Form):
    title = StringField(
        'Title',
        validators=DataRequired()
    )
    rating = SelectField(
        'Rating',
        choices=[('1', '2', '3', '4', '5')]
    )
    content = StringField(
        'Review',
        validators=DataRequired()
    )

class EditUserForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=(
                    "Username should be one word, letters, numbers, and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])

