from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, MultipleFileField,SelectField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo
from wtforms import ValidationError
from database import Database

def get_categories():
    categories = [None]
    
    with Database() as db:
        try:
            result = db.query("SELECT `sight_type_id`,`name` FROM `sight_type_meta` WHERE `language_id`= 1 ORDER BY sight_type_id")
        except:
            return [(1,"Error")]
        return result
def get_age_categories():
    with Database() as db:
        try:
            result = db.query("SELECT age_category_id,name FROM `age_category_meta` WHERE `language_id`= 1 ORDER BY age_category_id")
        except:
            return [(1,"Error")]
        return result


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

    
class TimeFormatValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u'Please enter the right format, for example: 12:38'
        self.message = message

    def __call__(self, form, field):
        time_str = field.data
        time_parts = time_str.split(':')
        if len(time_parts) != 2:
            raise ValidationError(self.message)
        hour, minute = time_parts
        if not hour.isdigit() or not minute.isdigit():
            raise ValidationError(self.message)
        if int(hour) < 0 or int(hour) > 23 or int(minute) < 0 or int(minute) > 59:
            raise ValidationError(self.message)


class Edit_sight_detail(FlaskForm):
    active = BooleanField("Active")
    sight_name = StringField("Sight Name",validators=[DataRequired()])
    age_category_id = SelectField("Age Category", choices=get_age_categories())
    #age_category_id = StringField("Age Category ID",validators=[DataRequired()])
    address = StringField("Address",validators=[DataRequired()])
    google_maps_url = StringField("Google Maps URL", validators=[])
    open_time = StringField("Open Time", validators=[TimeFormatValidator()])
    close_time = StringField("Close Time", validators=[TimeFormatValidator()])
    description = StringField("Description", validators=[])
    image = MultipleFileField("Image")
    old_sight_type = StringField("Old Sight type ID",validators=[DataRequired()])
    sight_type = SelectField("Category",choices=get_categories())
    #sight_type = StringField("Sight type ID",validators=[DataRequired()])
    submit = SubmitField("submit")


class Add_sight_form(FlaskForm):
    active = BooleanField("Active")
    sight_name = StringField("Sight Name",validators=[DataRequired()])
    age_category_id = StringField("Age Category ID",validators=[DataRequired()])
    address = StringField("Address",validators=[])
    google_maps_url = StringField("Google Maps URL", validators=[])
    open_time = StringField("Open Time", validators=[TimeFormatValidator()])
    close_time = StringField("Close Time", validators=[TimeFormatValidator()])
    description = StringField("Description", validators=[])
    image = MultipleFileField("Image")
    sight_type = StringField("Sight type ID",validators=[DataRequired()])
    submit = SubmitField("submit")



        
if __name__ == "__main__":
    get_categories()
    get_age_categories()
    