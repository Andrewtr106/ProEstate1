from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, EqualTo, Email

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(min=10, message='Description must be at least 10 characters')
    ])
    price = FloatField('Total Price (EGP)', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0, message='Price must be a positive number')
    ])
    property_type = SelectField('Property Type', choices=[
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Townhouse', 'Townhouse'),
        ('Penthouse', 'Penthouse'),
        ('Commercial', 'Commercial'),
        ('Land', 'Land')
    ], validators=[DataRequired(message='Property type is required')])
    location = StringField('Location', validators=[
        DataRequired(message='Location is required'),
        Length(min=3, max=200, message='Location must be between 3 and 200 characters')
    ])
    area = FloatField('Area (sqm)', validators=[
        DataRequired(message='Area is required'),
        NumberRange(min=1, message='Area must be greater than 0')
    ])
    bedrooms = IntegerField('Bedrooms', validators=[
        Optional(),
        NumberRange(min=0, message='Bedrooms must be a positive number')
    ])
    bathrooms = IntegerField('Bathrooms', validators=[
        Optional(),
        NumberRange(min=0, message='Bathrooms must be a positive number')
    ])
    down_payment = FloatField('Down Payment (EGP)', validators=[
        Optional(),
        NumberRange(min=0, message='Down payment must be a positive number')
    ])
    monthly_installment = FloatField('Monthly Installment (EGP)', validators=[
        Optional(),
        NumberRange(min=0, message='Monthly installment must be a positive number')
    ])
    installment_years = IntegerField('Installment Years', validators=[
        Optional(),
        NumberRange(min=1, max=30, message='Installment years must be between 1 and 30')
    ])
    image = FileField('Property Image', validators=[Optional()])
    submit = SubmitField('Add Property')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(min=10, max=20, message='Phone number must be between 10 and 20 digits')
    ])
    subject = StringField('Subject', validators=[
        Optional(),
        Length(max=200, message='Subject must not exceed 200 characters')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, message='Message must be at least 10 characters')
    ])
    submit = SubmitField('Send Message')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(min=10, max=20, message='Phone number must be between 10 and 20 digits')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required')
    ])
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(min=10, max=20, message='Phone number must be between 10 and 20 digits')
    ])
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required to make changes')
    ])
    new_password = PasswordField('New Password', validators=[
        Optional(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        Optional(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Update Profile')

class UserPropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(min=10, message='Description must be at least 10 characters')
    ])
    price = FloatField('Total Price (EGP)', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0, message='Price must be a positive number')
    ])
    property_type = SelectField('Property Type', choices=[
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Townhouse', 'Townhouse'),
        ('Penthouse', 'Penthouse'),
        ('Commercial', 'Commercial'),
        ('Land', 'Land')
    ], validators=[DataRequired(message='Property type is required')])
    location = StringField('Location', validators=[
        DataRequired(message='Location is required'),
        Length(min=3, max=200, message='Location must be between 3 and 200 characters')
    ])
    area = FloatField('Area (sqm)', validators=[
        DataRequired(message='Area is required'),
        NumberRange(min=1, message='Area must be greater than 0')
    ])
    bedrooms = IntegerField('Bedrooms', validators=[
        Optional(),
        NumberRange(min=0, message='Bedrooms must be a positive number')
    ])
    bathrooms = IntegerField('Bathrooms', validators=[
        Optional(),
        NumberRange(min=0, message='Bathrooms must be a positive number')
    ])
    down_payment = FloatField('Down Payment (EGP)', validators=[
        Optional(),
        NumberRange(min=0, message='Down payment must be a positive number')
    ])
    monthly_installment = FloatField('Monthly Installment (EGP)', validators=[
        Optional(),
        NumberRange(min=0, message='Monthly installment must be a positive number')
    ])
    installment_years = IntegerField('Installment Years', validators=[
        Optional(),
        NumberRange(min=1, max=30, message='Installment years must be between 1 and 30')
    ])
    image = FileField('Property Image', validators=[Optional()])
    submit = SubmitField('Add Property')
