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
    

    if request.method == "GET":
        return render_template("user_profile/user_profile.html")


@user_profile.route("/user-profile/settings", methods=["POST", "GET"])
@login_required
def user_profileSettings():
    if request.method =="GET":
        
        return render_template("user_profile/user_profile_settings.html", changePassForm = False)

@user_profile.route("/user-profile/settings/change-password", methods=["POST", "GET"])
@login_required
def user_profileSettingsChangePassword():
    user = current_user
    print(user)
    changePassForm = ChangePasswordForm()

    

    if request.method == "GET":
        
        
        return render_template("user_profile/user_profile_settings.html", changePassForm=changePassForm)

    else:
        if changePassForm.validate():
            oldPassword = changePassForm.oldPassword.data
            newPassword = changePassForm.newPassword.data
            verifyNewPassword = changePassForm.verifyNewPassword.data
            
            user = current_user
            success, message = user.changePassword(oldPassword, newPassword, verifyNewPassword)
            if success:
                return f"Succsesfully changes password !"
            else:
                flash(message)
                return render_template("user_profile/user_profile_settings.html", changePassForm=changePassForm)
        else:
            for errors in changePassForm.errors.values():
                for error in errors:
                    flash(error)
            return render_template("user_profile/user_profile_settings.html", changePassForm=changePassForm)

@user_profile.route("/user-profile/settings/change-username", methods=["POST", "GET"])
@login_required
def user_profileSettingsChangeUsername():
    user = current_user
    changeUserForm = ChangeUsername()
    