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

class EditProfileForm(Form):
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

class EditEmailForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])

class EditAddressForm(Form):
    street_address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = SelectField("State",validators=[DataRequired()], choices=[
        ('AL', 'AL'),
        ('AK','AK'),
        ('AR', 'AR'),
        ('AZ', 'AZ'),
        ('CA', 'CA'),
        ('CO', 'CO'),
        ('CT', 'CT'),
        ('DE', 'DE'),
        ('FL', 'FL'),
        ('GA', 'GA'),
        ('HI', 'HI'),
        ('ID', 'ID'),
        ('IL', 'IL'),
        ('IN', 'IN'),
        ('IA', 'IA'),
        ('KS', 'KS'),
        ('KY', 'KY'),
        ('LA', 'LA'),
        ('ME', 'ME'),
        ('MD', 'MD'),
        ('MA', 'MA'),
        ('MI', 'MI'),
        ('MN', 'MN'),
        ('MS', 'MS'),
        ('MO', 'MO'),
        ('MT', 'MT'),
        ('NE', 'NE'),
        ('NV', 'NV'),
        ('NH', 'NH'),
        ('NJ', 'NJ'),
        ('NM', 'NM'),
        ('NY', 'NY'),
        ('NC', 'NC'),
        ('ND', 'ND'),
        ('OH', 'OH'),
        ('OK', 'OK'),
        ('OR', 'OR'),
        ('PA', 'PA'),
        ('RI', 'RI'),
        ('SC', 'SC'),
        ('SD', 'SD'),
        ('TN', 'TN'),
        ('TX', 'TX'),
        ('UT', 'UT'),
        ('VT', 'VT'),
        ('VA', 'VA'),
        ('WA', 'WA'),
        ('WV', 'WV'),
        ('WI', 'WI'),
        ('WY', 'WY')
    ])
    postal_code = StringField(
        "ZIP Code", 
        validators=[
            DataRequired(),
            Regexp(
                r'^(\d{5})$',
                message=("Must be a five digit ZIP Code.")
    )])

class ReviewForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[('5', '5'), ('4','4'), ('3', '3'), ('2', '2'), ('1', '1')])
    content = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField("Submit")

class EditReviewForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[('5', '5'), ('4','4'), ('3', '3'), ('2', '2'), ('1', '1')])
    content = TextAreaField('Review', validators=[DataRequired()])

class ShippingForm(Form):
    recipient_fname = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z_]+$',
                message=("Cannot contain numbers or special characters")
            )
        ]
    )
    recipient_lname = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z_]+$',
                message=("Cannot contain numbers or special characters")
            )
        ]
    )
    recipient_street_address = StringField("Address", validators=[DataRequired()])
    recipient_city = StringField("City", validators=[DataRequired()])
    recipient_state = SelectField("State",validators=[DataRequired()], choices=[
                ('AL', 'AL'),
        ('AK','AK'),
        ('AR', 'AR'),
        ('AZ', 'AZ'),
        ('CA', 'CA'),
        ('CO', 'CO'),
        ('CT', 'CT'),
        ('DE', 'DE'),
        ('FL', 'FL'),
        ('GA', 'GA'),
        ('HI', 'HI'),
        ('ID', 'ID'),
        ('IL', 'IL'),
        ('IN', 'IN'),
        ('IA', 'IA'),
        ('KS', 'KS'),
        ('KY', 'KY'),
        ('LA', 'LA'),
        ('ME', 'ME'),
        ('MD', 'MD'),
        ('MA', 'MA'),
        ('MI', 'MI'),
        ('MN', 'MN'),
        ('MS', 'MS'),
        ('MO', 'MO'),
        ('MT', 'MT'),
        ('NE', 'NE'),
        ('NV', 'NV'),
        ('NH', 'NH'),
        ('NJ', 'NJ'),
        ('NM', 'NM'),
        ('NY', 'NY'),
        ('NC', 'NC'),
        ('ND', 'ND'),
        ('OH', 'OH'),
        ('OK', 'OK'),
        ('OR', 'OR'),
        ('PA', 'PA'),
        ('RI', 'RI'),
        ('SC', 'SC'),
        ('SD', 'SD'),
        ('TN', 'TN'),
        ('TX', 'TX'),
        ('UT', 'UT'),
        ('VT', 'VT'),
        ('VA', 'VA'),
        ('WA', 'WA'),
        ('WV', 'WV'),
        ('WI', 'WI'),
        ('WY', 'WY')
    ])
    recipient_postal_code = StringField(
        "ZIP Code", 
        validators=[
            DataRequired(),
            Regexp(
                r'^(\d{5})$',
                message=("Must be a five digit ZIP Code.")
    )])
