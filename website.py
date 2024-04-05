from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
import secrets
from user import User

from sight.sight import sight
from reglog.reglog import reglog
from user_profile.user_profile import user_profile
from admin.admin import admin

import random as rand
from database import  Database
from models.sight import Sight
from config.email import *


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

UPLOAD_PATH = 'static/images/sight'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "/reglog/login"

csrf = CSRFProtect(app)

app.register_blueprint(sight, url_prefix="/sight")
app.register_blueprint(reglog, url_prefix="/reglog")
app.register_blueprint(user_profile, url_prefix="/user-profile")
app.register_blueprint(admin, url_prefix="/admin")


@loginManager.user_loader
def load_user(user_id):
    return User().get_user_by_id(user_id)

@app.route("/")
def index():

    with Database(dict_cursor=True) as db:
        sight_model = Sight(db)
        sights = sight_model.getAllSights()
    
    admin = False
    if current_user.is_authenticated:
        user = current_user
        admin = True if user.check_if_user_is_admin() else False

    return render_template("index.html", sights=(rand.sample(sights,3)), admin=admin)

if __name__ == "__main__":
    app.run(debug=True)
