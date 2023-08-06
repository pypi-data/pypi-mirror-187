from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from openwebpos.blueprints.user.models import Role


class LoginForm(FlaskForm):
    """
    Login Form

    Extends:
        FlaskForm

    Variables:
        email {StringField} -- Email field
        password {PasswordField} -- Password field
        remember_me {BooleanField} -- Remember me field
        submit {SubmitField} -- Submit button

    Returns:
        LoginForm -- Login form

    Example:
        >>> form = LoginForm()
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class StaffLoginForm(FlaskForm):
    """
    Staff Login Form

    Extends:
        FlaskForm

    Variables:
        pin {PasswordField} -- Pin field
        submit {SubmitField} -- Submit button

    Returns:
        StaffLoginForm -- Staff login form

    Example:
        >>> form = StaffLoginForm()
    """
    pin = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=15,
               message="Password needs to be between 4 - 15 digits.")])
    submit = SubmitField('Login')


class AddUserForm(FlaskForm):
    """
    Form to add a user.

    Extends:
        FlaskForm

    Variables:
        username {StringField} -- Username field
        email {StringField} -- Email field
        password {PasswordField} -- Password field
        confirm_password {PasswordField} -- Confirm password field
        submit {SubmitField} -- Submit button

    Returns:
        AddUserForm -- Add user form

    Example:
        >>> form = AddUserForm()
    """
    role = SelectField('Role', coerce=int)
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Submit')

    def set_choices(self):
        """Set choices for user roles."""
        roles = Role.query.filter_by(active=True).all()
        self.role.choices = [(role.id, role.name) for role in roles]


class UserProfileForm(FlaskForm):
    """
    Form to update a user's profile.

    Extends:
        FlaskForm

    Variables:
        first_name {StringField} -- First name field
        last_name {StringField} -- Last name field
        phone {StringField} -- Phone field
        address {StringField} -- Address field
        city {StringField} -- City field
        state {StringField} -- State field
        zip_code {StringField} -- Zip code field
        dob {StringField} -- Date of birth field
        submit {SubmitField} -- Submit button

    Returns:
        UserProfileForm -- User profile form

    Example:
        >>> form = UserProfileForm()
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    dob = StringField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Submit')
