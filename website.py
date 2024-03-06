from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
import secrets
from forms import LoginForm, RegistrationForm
from user import User

from sight.sight import sight


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


csrf = CSRFProtect(app)

app.register_blueprint(sight, url_prefix="/sight")


#loginManager = LoginManager()
#loginManager.init_app(app)
#loginManager.login_view = "/login"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
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
                return render_template("login.html")
        else:
            for errors in loginForm.errors.values():
                for error in errors:
                    flash(error)
            return redirect(url_for("login"))


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")

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
                return render_template("signup.html")
        else:
            for errors in registrationForm.errors.values():
                for error in errors:
                    flash(error)
            return redirect(url_for("sign_up"))


if __name__ == "__main__":
    app.run(debug=True)
