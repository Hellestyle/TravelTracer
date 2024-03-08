from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from forms import LoginForm, RegistrationForm
from user import User
from flask import flash

from website import load_user



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
            success, message = user.login(email, password)
            if success:
                user = load_user(email)
                return f"{user}"
            else:
                flash(message)
                return render_template("reglog/login.html", login=loginForm)
        else:
            for errors in loginForm.errors.values():
                for error in errors:
                    flash(error)
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
