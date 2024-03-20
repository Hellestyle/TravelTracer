from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from forms import LoginForm, RegistrationForm
from user import User
from flask import flash
from app_email import send_email
from config.application import APPLICATION_URL

import sys


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

            user_model = User()
            user = user_model.get_user_by_email(email)
            if user is not None and user.check_password(password):

                if user.isVerified():

                    login_user(user, force=True)
                    next = request.args.get('next')
                    if next is None or not next.startswith('/'):
                        next = url_for('index')
                    return redirect(next)
                
                else:
                    return render_template(
                        "reglog/email_sent.html",
                        title="Verify your email adress",
                        message=f"We have sent you an email with a link to {email} to verify your email address. Please check your inbox and click the link to verify your email address.",
                        link=f"{APPLICATION_URL}/reglog/resend/{user.get_id()}",
                        link_title="Resend verification email"
                    )
            
            else:
                flash("Invalid email or password")
                return render_template("reglog/login.html", login=loginForm)
        
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
                user_model = User()
                usr = user_model.get_user_by_email(email)
                send_email(current_app, [email], "Registration Verification", render_template(
                    "reglog/email.html",
                    title="Verify your email adress",
                    message="To verify your email address, please click the link below.",
                    link=f"{APPLICATION_URL}/reglog/verify/{usr.get_verification_uuid()}",
                    link_title="Verify email address"
                ))
                return render_template(
                    "reglog/email_sent.html",
                    title="Verify your email adress",
                    message=f"We have sent you an email with a link to {email} to verify your email address. Please check your inbox and click the link to verify your email address.",
                    link=f"{APPLICATION_URL}/reglog/resend/{usr.get_id()}",
                    link_title="Resend verification email"
                )
                # login_user(usr, force=True)
                # return redirect(url_for('index'))
            else:
                flash(message)
                return render_template("reglog/signup.html", form=registrationForm)
        else:
            for errors in registrationForm.errors.values():
                for error in errors:
                    flash(error)
            return render_template("reglog/signup.html", form=registrationForm)


@reglog.route("/verify/<uuid>")
def verify(uuid):

    user = User()

    success, message, user = user.verify(uuid)

    if success:

        login_user(user, force=True)

        return redirect(url_for('user_profile.user_profileMain'))
    
    else:
        return message
    

@reglog.route("/resend/<int:user_id>")
def resend(user_id):

    user = User().get_user_by_id(user_id)
    
    success, message = user.update_uuid()

    if success:

        email = user.get_email()

        send_email(current_app, [email], "Registration Verification", render_template(
            "reglog/email.html",
            title="Verify your email adress",
            message="To verify your email address, please click the link below.",
            link=f"{APPLICATION_URL}/reglog/verify/{user.get_verification_uuid()}",
            link_title="Verify email address"
        ))

        return render_template(
            "reglog/email_sent.html",
            title="Verify your email adress",
            message=f"We have sent you an email with a link to {email} to verify your email address. Please check your inbox and click the link to verify your email address.",
            link=f"{APPLICATION_URL}/reglog/resend/{user_id}",
            link_title="Resend verification email"
        )

    else:
        return message


@reglog.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))