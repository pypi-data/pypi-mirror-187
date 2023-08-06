from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class DatabaseConfigForm(FlaskForm):
    dialect = SelectField(choices=[('sqlite', 'SQLite'), ('mysql', 'MySQL'),
                                   ('postgresql', 'PostgreSQL')])
    username = StringField('Username')
    password = PasswordField('Password')
    password2 = PasswordField('Confirm Password',
                              validators=[EqualTo('password')])
    host = StringField('Host')
    port = StringField('Port')
    database = StringField('Database')
