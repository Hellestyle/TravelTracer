from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
import secrets
from forms import LoginForm, RegistrationForm
from user import User

from sight.sight import sight
from reglog.reglog import reglog
from user.user import user


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


csrf = CSRFProtect(app)

app.register_blueprint(sight, url_prefix="/sight")
app.register_blueprint(reglog, url_prefix="/reglog")
app.register_blueprint(user, url_prefix="/user")


#loginManager = LoginManager()
#loginManager.init_app(app)
#loginManager.login_view = "/login"


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
