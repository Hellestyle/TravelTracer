from forms import ChangePasswordForm
from flask import Blueprint, render_template, request, redirect, url_for, flash

from user import User
from flask import flash


user_profile = Blueprint("user_profile", __name__, template_folder="templates", static_folder="static")

@user_profile.route("/user_profile", methods=["POST", "GET"])
@login_required
def user_profileChangePassword(user):
    changePassowordForm = ChangePasswordForm(request.form)

    if request.method == "GET":
        return render_template("user_profile/user_profile.html", form=changePassowordForm)

    else:
        if changePassowordForm.validate():
            oldPassword = changePassowordForm.oldPassword.data
            newPassword = changePassowordForm.newPassword.data
            verifyNewPassword = changePassowordForm.verifyNewPassword.data
            
            #Må ha logged_in User objekt før man kan gå videre
            success, message = user.changePassword(oldPassword, newPassword, verifyNewPassword)
            if success:
                return f"Succsesfully changes password !"
            else:
                flash(message)
                return render_template("user_profile/user_profile.html", form=changePassowordForm)
        else:
            for errors in changePassowordForm.errors.values():
                for error in errors:
                    flash(error)
            return render_template("user_profile/user_profile.html", form=changePassowordForm)