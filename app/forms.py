from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[InputRequired(), Length(max=30)])
    password = PasswordField('Password', render_kw={"placeholder": "Password"}, validators=[InputRequired(), Length(min=8, max=30, message="Password must be between 8 and 30 characters.")])
    confirm_password = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm Password"}, validators=[InputRequired(), EqualTo('password', message="Passwords must match.")])


class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[InputRequired()])
    password = PasswordField('Password', render_kw={"placeholder": "Password"}, validators=[InputRequired()])


class ChangeUserForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=30)])
    password = PasswordField('Password', validators=[InputRequired()])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired(message="This field is required.")])
    new_password = PasswordField('New Password', validators=[InputRequired(message="This field is required.")])
    confirm_new_password = PasswordField('Confirm New Password', validators=[InputRequired(message="This field is required.")])