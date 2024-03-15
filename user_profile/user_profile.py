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
    changePassForm = ChangePasswordForm()
    changeUserForm = ChangeUsername()
    if request.method == "GET":
        return render_template("user_profile/user_profile.html", changePassForm=changePassForm, changeUserForm=changeUserForm)

    else:
        if changePassForm.submitPasswordChange.data and changePassForm.validate():
            # Do change password with func
            oldPassword = changePassForm.oldPassword.data
            newPassword = changePassForm.newPassword.data
            verifyNewPassword = changePassForm.verifyNewPassword.data
            
            user = current_user
            success, message = user.changePassword(oldPassword, newPassword, verifyNewPassword)
            if success:
                return f"Succsesfully changes password !"
            else:
                flash(message)
                return render_template("user_profile/user_profile.html", changePassForm=changePassForm,changeUserForm=changeUserForm)
        elif changeUserForm.submitUsernameChange.data and changeUserForm.validate():
            # do change username with func
            return print(current_user)
        else:
            if changePassForm.errors:
                for errors in changePassForm.errors.values():
                    for error in errors:
                        flash(error)
            else:
                for errors in changeUserForm.errors.values():
                    for error in errors:
                        flash(error)
            return render_template("user_profile/user_profile.html", changePassForm=changePassForm,changeUserForm=changeUserForm)


@user_profile.route("/user-profile/settings/change-password", methods=["POST", "GET"])
@login_required
def user_profileSettingsChangePassword():
    user = current_user
    print(user)
    changePassForm = ChangePasswordForm()
    changeUserForm = ChangeUsername()

    

    if request.method == "GET":
        
        
        return render_template("user_profile/user_profile.html", changePassForm=changePassForm,changeUserForm=changeUserForm)

    else:
        if changePassForm.submitPasswordChange.data and changePassForm.validate():
            oldPassword = changePassForm.oldPassword.data
            newPassword = changePassForm.newPassword.data
            verifyNewPassword = changePassForm.verifyNewPassword.data
            
            user = current_user
            success, message = user.changePassword(oldPassword, newPassword, verifyNewPassword)
            if success:
                return f"Succsesfully changes password !"
            else:
                flash(message)
                return render_template("user_profile/user_profile.html", changePassForm=changePassForm,changeUserForm=changeUserForm)
        else:
            for errors in changePassForm.errors.values():
                for error in errors:
                    flash(error)
            return render_template("user_profile/user_profile.html", changePassForm=changePassForm,changeUserForm=changeUserForm)

@user_profile.route("/user-profile/settings/change-username", methods=["POST", "GET"])
@login_required
def user_profileSettingsChangeUsername():
    user = current_user
    changeUserForm = ChangeUsername()
    changePassForm = ChangePasswordForm()
    