from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(3, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email])
    username = StringField("Username", validators=[DataRequired, Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("password2", message="Passwords must match.")])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    first_name = StringField("First name", validators=[InputRequired])
    last_name = StringField("Last name", validators=[InputRequired])
    submit = SubmitField('Register')

    def validate_email(self, field):
        #Sqlspørring som sjekker om mail adressen allerede er i bruk
            raise ValidationError("Email already registered")
    
    def validate_username(self, field):
         #Sql spørring som sjekker om brukernavn allerede er registrert
            raise ValidationError("Username already registered")
         
