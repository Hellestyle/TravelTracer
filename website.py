from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

#csrf = CSRFProtect(app)

#loginManager = LoginManager()
#loginManager.init_app(app)
#loginManager.login_view = "/login"

@app.route('/')
def index():
    return render_template("auth/login.html")





if __name__ == "__main__":
    app.run(debug=True)