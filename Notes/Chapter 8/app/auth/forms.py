from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Length(1, 64),
                                    Email()])
    username = StringField('Username', 
                           validators=[DataRequired(), 
                                       Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, numbers, dots or '
                                              'underscores')])
    password = PasswordField('Password', 
                             validators=[DataRequired(),
                                         EqualTo('password2', 
                                                 message='Passwords must match.')])
    password2 = PasswordField('Confirm password', 
                              validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
        
    def validate_password(self, field): 
        password = field.data
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """

        # calculating the length
        length_error = len(password) < 8
        import regex as re
        # searching for digits
        digit_error = re.search(r"\d", password) is None

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None

        # searching for symbols
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

        # overall result
        password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

        return {
            'password_ok' : ValidationError(password_ok),
            'length_error' : ValidationError(length_error),
            'digit_error' : ValidationError(digit_error),
            'uppercase_error' : ValidationError(uppercase_error),
            'lowercase_error' : ValidationError(lowercase_error),
            'symbol_error' : ValidationError(symbol_error),
        }

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')