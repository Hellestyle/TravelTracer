from flask import Blueprint, render_template, request, redirect, url_for, flash

from forms import LoginForm, RegistrationForm
from user import User


reglog = Blueprint("reglog", __name__, template_folder="templates", static_folder="static")


@reglog.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "GET":
        return render_template("reglog/login.html")
    
    else:
        loginForm = LoginForm(request.form)

        if loginForm.validate():
            email = loginForm.email.data
            password = loginForm.password.data

            user = User()
            success, message = user.login(email, password)
            if success:
                return f"{user}"
            else:
                flash(message)
                return render_template("reglog/login.html")
        else:
            for errors in loginForm.errors.values():
                for error in errors:
                    flash(error)
            return redirect(url_for("reglog.login"))


@reglog.route("/signup", methods=["POST", "GET"])
def sign_up():

    registrationForm = RegistrationForm(request.form)

    if request.method == "GET":
        return render_template("reglog/signup.html", form=registrationForm)

    else:
        registrationForm = RegistrationForm(request.form)

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
