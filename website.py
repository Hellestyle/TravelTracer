from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
import secrets
from forms import LoginForm, RegistrationForm
from user import User

from sight.sight import sight
from reglog.reglog import reglog
from user_profile.user_profile import user_profile


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


csrf = CSRFProtect(app)

app.register_blueprint(sight, url_prefix="/sight")
app.register_blueprint(reglog, url_prefix="/reglog")
app.register_blueprint(user_profile, url_prefix="/user-profile")


#loginManager = LoginManager()
#loginManager.init_app(app)
#loginManager.login_view = "/login"


@app.route("/")
def index():
    sights=[
            {'name': 'Eiffel Tower'},
            {'name': 'Statue of Liberty'},
            {'name': 'Great Wall of China'},
            {'name': 'Taj Mahal'},
            {'name': 'Pyramids of Giza'},
            {'name': 'Colosseum'},
            {'name': 'Machu Picchu'},
            {'name': 'Stonehenge'},
            {'name': 'Petra'},
            {'name': 'Chichen Itza'},
            {'name': 'Christ the Redeemer'},
            {'name': 'Angkor Wat'}
            ]
    return render_template("index.html", sights=sights)


if __name__ == "__main__":
    app.run(debug=True)
