from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from forms import LoginForm, RegistrationForm
from models.user import User
from flask import flash
from app_email import send_email
from config.application import APPLICATION_URL

import sys
from uuid import uuid4


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
                        tab_title="Email Verification",
                        title="Check your inbox",
                        message=f"Click on the link we sent to {email} to finish your account setup. No email in your inbox or spam folder? Let's resend it.",
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
                send_email(current_app, [email], "Verify your email address", render_template(
                    "reglog/email.html",
                    title="Verify your email address",
                    message="To start using TravelTracer, just click the verify email button below:",
                    link=f"{APPLICATION_URL}/reglog/verify/{usr.get_verification_uuid()}",
                    link_title="Verify email"
                ))
                return render_template(
                    "reglog/email_sent.html",
                    tab_title="Email Verification",
                    title="Check your inbox",
                    message=f"Click on the link we sent to {email} to finish your account setup. No email in your inbox or spam folder? Let's resend it.",
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

        send_email(current_app, [email], "Verify your email address", render_template(
            "reglog/email.html",
            title="Verify your email address",
            message="To start using TravelTracer, just click the verify email button below.",
            link=f"{APPLICATION_URL}/reglog/verify/{user.get_verification_uuid()}",
            link_title="Verify email"
        ))

        return render_template(
            "reglog/email_sent.html",
            tab_title="Email Verification",
            title="Check your inbox",
            message=f"Click on the link we sent to {email} to finish your account setup. No email in your inbox or spam folder? Let's resend it.",
            link=f"{APPLICATION_URL}/reglog/resend/{user_id}",
            link_title="Resend verification email"
        )

    else:
        return message


@reglog.route("/password-recovery", methods=["POST", "GET"])
def password_recovery():
    
    if request.method == "GET":
        return render_template("reglog/password_recovery.html", uuid=None)

    else:
        
        email = request.form.get("email")

        user = User().get_user_by_email(email)

        if user is not None:

            password_recovery_uuid = str(uuid4())

            success, message = user.add_password_recovery_uuid(password_recovery_uuid)

            if success:

                send_email(current_app, [email], "Password Recovery", render_template(
                    "reglog/email.html",
                    title="Forgot your password? It happens to the best of us.",
                    message="To reset your password, click the link below.",
                    link=f"{APPLICATION_URL}/reglog/password-recovery/{password_recovery_uuid}",
                    link_title="Reset your password"
                ))

                return render_template(
                    "reglog/email_sent.html",
                    tab_title="Password Recovery",
                    title="Check your inbox",
                    message=f"If an account exists for {email}, you will get an email with instructions on resetting your password. If it doesn't arrive, be sure to check your spam folder.",
                    link=f"{APPLICATION_URL}/reglog/resend-password-recovery/{user.get_id()}",
                    link_title="Resend password recovery email"
                )

            else:

                flash(message)

                return render_template("reglog/password_recovery.html", uuid=None)

        else:

            flash(f"User with email {email} does not exist.")

            return render_template("reglog/password_recovery.html", uuid=None)
    

@reglog.route("/password-recovery/<uuid>", methods=["POST", "GET"])
def password_recovery_verify(uuid):

    user = User().get_user_by_password_recovery_uuid(uuid)

    if user is None:
        return "Invalid password recovery link.", 404

    if request.method == "GET":
        return render_template("reglog/password_recovery.html", uuid=uuid)

    else:

        uuid = request.form.get("uuid")

        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        if password == password_confirmation:

            success, message = user.recover_password(password)

            if success:

                flash("Password has been changed.")

                return render_template("reglog/login.html", login=LoginForm())

            else:

                flash(message)

                return render_template("reglog/password_recovery.html", uuid=uuid)

        else:

            flash("Passwords do not match.")

            return render_template("reglog/password_recovery.html", uuid=uuid)


@reglog.route("/resend-password-recovery/<int:user_id>")
def resend_password_recovery(user_id):

    user = User().get_user_by_id(user_id)

    if user is None:
        return "Invalid user.", 404

    password_recovery_uuid = str(uuid4())

    success, message = user.add_password_recovery_uuid(password_recovery_uuid)

    if success:

        email = user.get_email()

        send_email(current_app, [email], "Password Recovery", render_template(
            "reglog/email.html",
            title="Forgot your password? It happens to the best of us.",
            message="To reset your password, click the link below.",
            link=f"{APPLICATION_URL}/reglog/password-recovery/{password_recovery_uuid}",
            link_title="Reset your password"
        ))

        return render_template(
            "reglog/email_sent.html",
            tab_title="Password Recovery",
            title="Check your inbox",
            message=f"If an account exists for {email}, you will get an email with instructions on resetting your password. If it doesn't arrive, be sure to check your spam folder.",
            link=f"{APPLICATION_URL}/reglog/resend-password-recovery/{user_id}",
            link_title="Resend password recovery email"
        )

    else:

        return message


@reglog.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))