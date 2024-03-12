from forms import ChangePasswordForm, ChangeUsername
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from user import User
from flask import flash


user_profile = Blueprint("user_profile", __name__, template_folder="templates", static_folder="static")

@user_profile.route("/user-profile", methods=["POST", "GET"])
@login_required
def user_profileMain():
    user = current_user
    changePassowordForm = ChangePasswordForm(request.form)
    changeUsernameForm = ChangeUsername(request.form)

    if request.method == "GET":
        return render_template("user_profile/user_profile.html", changePassowordForm=changePassowordForm)

    else:
        if changePassowordForm.validate():
            oldPassword = changePassowordForm.oldPassword.data
            newPassword = changePassowordForm.newPassword.data
            verifyNewPassword = changePassowordForm.verifyNewPassword.data
            
            user = current_user
            success, message = user.changePassword(oldPassword, newPassword, verifyNewPassword)
            if success:
                return f"Succsesfully changes password !"
            else:
                flash(message)
                return render_template("user_profile/user_profile.html", changePassowordForm=changePassowordForm)
        else:
            for errors in changePassowordForm.errors.values():
                for error in errors:
                    flash(error)
            return render_template("user_profile/user_profile.html", changePassowordForm=changePassowordForm)

@user_profile.route("/user-profile/settings", methods=["POST", "GET"])
@login_required
def user_profileSettings():
    user = current_user
    print(user)
    changePassowordForm = ChangePasswordForm()
    changeUsernameForm = ChangeUsername()

    if request.method == "GET":
        changePassowordForm = ChangePasswordForm()
        changeUsernameForm = ChangeUsername()
        return render_template("user_profile/user_profile_settings.html", changePassowordForm=changePassowordForm,changeUsernameForm=changeUsernameForm)

    else:
        if changePassowordForm.validate():
            oldPassword = changePassowordForm.oldPassword.data
            newPassword = changePassowordForm.newPassword.data
            verifyNewPassword = changePassowordForm.verifyNewPassword.data
            
            user = current_user
            success, message = user.changePassword(oldPassword, newPassword, verifyNewPassword)
            if success:
                return f"Succsesfully changes password !"
            else:
                flash(message)
                return render_template("user_profile/user_profile_settings.html", changePassowordForm=changePassowordForm,changeUsernameForm=changeUsernameForm)
        else:
            for errors in changePassowordForm.errors.values():
                for error in errors:
                    flash(error)
            return render_template("user_profile/user_profile_settings.html", changePassowordForm=changePassowordForm, changeUsernameForm=changeUsernameForm)
    