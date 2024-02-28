from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
import secrets
from forms import LoginForm, RegistrationForm
from user import User


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


csrf = CSRFProtect(app)


#loginManager = LoginManager()
#loginManager.init_app(app)
#loginManager.login_view = "/login"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    loginform = LoginForm()
    
    if loginform.validate_on_submit():
    #if request.method == "POST":
        print("HEIOA")
        email = loginform.email.data
        password = loginform.password.data
        user = User()
        user.login(email,password)
        return f'{user}'
    
    if request.method == "GET":
        return render_template("login.html",loginform = loginform)


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
