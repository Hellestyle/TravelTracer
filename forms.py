from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo
from wtforms import ValidationError
from database import Database


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(message="Please enter your email"), Email(message="Email must use email format")])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(message="Please enter your email"), Length(min=5, max=100), Email(message="Email must use the email format")])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=30, message="Password must contain at least 8 characters")])
    verify_password = PasswordField('verify_password', validators=[EqualTo('password', message="The two passwords must match")])
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=45, message="Username must contain at least 3 characters")])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    submit = SubmitField('submit')
    
class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField("Old Password",validators=[DataRequired(), Length(min=8, max=30, message="Password must contain at least 8 characters")])
    newPassword = PasswordField("New Password",validators=[DataRequired(), Length(min=8, max=30, message="Password must contain at least 8 characters")])
    verifyNewPassword = PasswordField('Confirm Password', validators=[EqualTo('newPassword', message="The two passwords must match")])
    submitPasswordChange = SubmitField("Change Password")

class ChangeUsername(FlaskForm):
    newUsername = StringField('New Username', validators=[DataRequired(), Length(min=3, max=30, message="Username must contain at least 3 characters")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30, message="Password must contain at least 8 characters")])
    newFirstName = StringField('New First Name', validators=[DataRequired()])
    newLastName = StringField('New Last Name', validators=[DataRequired()])
    submitUsernameChange = SubmitField("Save changes")

class ChangePrivacySettings(FlaskForm):
    openProfile = BooleanField("Open profile")
    showFriendslist = BooleanField("Show friendslist")
    showRealName = BooleanField("Show Real Name")
    submitPrivacySettings = SubmitField("Save")
    
class EditSight(FlaskForm):
    city_id = StringField("City ID", validators=[DataRequired()])
    age_category_id = StringField("Age Category ID",validators=[DataRequired()])
    google_maps_url = StringField("Google Maps Url")
    active = BooleanField("Active sight",validators=[DataRequired()])
    open_time = StringField("Open time")
    close_time = StringField("Close time")
    sight_type = StringField("Sight type ID",validators=[DataRequired()])
    sight_name = StringField("Sight Name",validators=[DataRequired()])
    sight_desc = StringField("Sight Description")
    sight_address = StringField("Sight Adress")
    sight_photo = StringField("Sight photo")
    
    