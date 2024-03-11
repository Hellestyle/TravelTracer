from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from forms import LoginForm, RegistrationForm
from user import User
from flask import flash




reglog = Blueprint("reglog", __name__, template_folder="templates", static_folder="static")



@reglog.route("/login", methods=["POST", "GET"])
def login():
    loginForm = LoginForm(request.form)

    if request.method == "GET":
        return render_template("reglog/login.html", login=loginForm)
    
    else:
        if loginForm.validate():
            email = loginForm.email.data
            password = loginForm.password.data

            user = User()
            usr = user.get_email(email)
            if usr and usr.check_password(password):
                login_user(user, remember=True)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('index')
                return redirect(next)
            
            flash("Invalid email or password")
                
        return render_template("reglog/login.html", login=loginForm)


@reglog.route("/signup", methods=["POST", "GET"])
def sign_up():
    registrationForm = RegistrationForm(request.form)

    if request.method == "GET":
        return render_template("reglog/signup.html", form=registrationForm)

    else:
        if registrationForm.validate():
            email = registrationForm.email.data
            password = registrationForm.password.data
            username = registrationForm.username.data
            firstName = registrationForm.first_name.data
            lastName = registrationForm.last_name.data

            user = User()
            success, message = user.registrer(firstName, lastName, email, username, password)
            if success:
                return f"Welcome {username}!"
            else:
                flash(message)
                return render_template("reglog/signup.html", form=registrationForm)
        else:
            for errors in registrationForm.errors.values():
                for error in errors:
                    flash(error)
            return render_template("reglog/signup.html", form=registrationForm)
