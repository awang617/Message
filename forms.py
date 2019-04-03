from flask_wtf import FlaskForm as Form

from models import User

from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp, ValidationError, Length, EqualTo, Email

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
                message=("Cannot contain numbers or special characters")
            )
        ]
    )
    lname = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z_]+$',
                message=("Cannot contain numbers or special characters")
            )
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
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
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class ReviewForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[('1', '1'), ('2','2'), ('3', '3'), ('4', '4'), ('5', '5')])
    content = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField("Submit")



