from forms import ChangePasswordForm, ChangeUsername, ChangePrivacySettings
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
    changePrivacySettingsForm = ChangePrivacySettings()
    
    result_01, user_info = user.get_user_info()
    result_02, friend_amount = user.get_friend_amount()
    result_03, friend_list = user.get_friendlist()
    
    

    if request.method == "GET":
        result_01, user_info = user.get_user_info()
        result_02, friend_amount = user.get_friend_amount()
        result_03, friend_list = user.get_friendlist()
        result_04, friend_requests = user.get_friend_requests()

        if result_01 and result_02 and result_03 and result_04:
            return render_template("user_profile/user_profile.html", \
                                changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                user_info=user_info, friend_amount=friend_amount, \
                                friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm
                            )
        else:
            if result_01 is False:
                flash(user_info)
            elif result_02 is False:
                flash(friend_amount)
            else:
                flash(friend_list)
            return render_template("user_profile/user_profile.html", \
                                changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                user_info=user_info, friend_amount=friend_amount, \
                                friend_list=friend_list, friend_requests=friend_requests,changePrivacySettingsForm=changePrivacySettingsForm
                            )

    else:
        if changePassForm.submitPasswordChange.data and changePassForm.validate():
            # Password change
            oldPassword = changePassForm.oldPassword.data
            newPassword = changePassForm.newPassword.data
            verifyNewPassword = changePassForm.verifyNewPassword.data
            
            user = current_user
            success, message = user.changePassword(oldPassword, newPassword, verifyNewPassword)
            if success:
                message = "Succsesfully changed password !"
                flash(message)
                return render_template("user_profile/user_profile.html", changePassForm=changePassForm, changeUserForm=changeUserForm, user_info=user_info, friend_amount=friend_amount, friend_list=friend_list, changePrivacySettingsForm=changePrivacySettingsForm)
            else:
                flash(message)
                return render_template("user_profile/user_profile.html", changePassForm=changePassForm, changeUserForm=changeUserForm, user_info=user_info, friend_amount=friend_amount, friend_list=friend_list, changePrivacySettingsForm=changePrivacySettingsForm)
            

        elif changeUserForm.submitUsernameChange.data and changeUserForm.validate():
            # Username and Name change 
            newUsername = changeUserForm.newUsername.data
            password = changeUserForm.password.data
            newFirstName = changeUserForm.newFirstName.data
            newLastName = changeUserForm.newLastName.data
            
            user = current_user
            success, message = user.changeNames(password,newUsername,newFirstName,newLastName)
            if success:
                message = "Succsesfully changed User names !"
                flash(message)
                return render_template("user_profile/user_profile.html", changePassForm=changePassForm, changeUserForm=changeUserForm, user_info=user_info, friend_amount=friend_amount, friend_list=friend_list, changePrivacySettingsForm=changePrivacySettingsForm)
            else:
                flash(message)
                return render_template("user_profile/user_profile.html", changePassForm=changePassForm, changeUserForm=changeUserForm, user_info=user_info, friend_amount=friend_amount, friend_list=friend_list, changePrivacySettingsForm=changePrivacySettingsForm)
            

        
        elif changePrivacySettingsForm.submitPrivacySettings.data and changePrivacySettingsForm.validate():
            # Privacy settings change
            success, message = user.updatePrivacySettings( changePrivacySettingsForm.openProfile.data,changePrivacySettingsForm.showFriendslist.data,changePrivacySettingsForm.showRealName.data)
            if success:
                message = "Succsesfully changed privacy settings !"
                flash(message)
                return render_template("user_profile/user_profile.html", changePassForm=changePassForm, changeUserForm=changeUserForm, user_info=user_info, friend_amount=friend_amount, friend_list=friend_list, changePrivacySettingsForm=changePrivacySettingsForm)
            else:
                flash(message)
                return render_template("user_profile/user_profile.html", changePassForm=changePassForm, changeUserForm=changeUserForm, user_info=user_info, friend_amount=friend_amount, friend_list=friend_list, changePrivacySettingsForm=changePrivacySettingsForm)
            
        
        # Error handling
        else:
            if changePassForm.errors:
                for errors in changePassForm.errors.values():
                    for error in errors:
                        flash(error)
            else:
                for errors in changeUserForm.errors.values():
                    for error in errors:
                        flash(error)
            return render_template("user_profile/user_profile.html", changePassForm=changePassForm, changeUserForm=changeUserForm, user_info=user_info, friend_amount=friend_amount, friend_list=friend_list, changePrivacySettingsForm=changePrivacySettingsForm)


@user_profile.route("/user-profile/accept-friend-request/<string:sender_name>", methods=["POST", "GET"])
@login_required
def accept_friend_request(sender_name):
    user = current_user

    result_01, users_info = user.get_usernames_and_user_id()
    if result_01:
        for user_info in users_info:
            if user_info["username"] == sender_name:
                sender_id = user_info["id"]
                break

        result_02, message = user.accept_friend_request(sender_id)
        flash(message)
        return redirect(url_for("user_profile.user_profileMain"))
            
    else:
        flash(users_info)
        return redirect(url_for("user_profile.user_profileMain"))


@user_profile.route("/user-profile/decline-friend-request/<string:sender_name>", methods=["POST", "GET"])
@login_required
def decline_friend_request(sender_name):
    user = current_user

    result_01, users_info = user.get_usernames_and_user_id()
    if result_01:
        for user_info in users_info:
            if user_info["username"] == sender_name:
                sender_id = user_info["id"]
                break

        result_02, message = user.decline_friend_request(sender_id)
        flash(message)
        return redirect(url_for("user_profile.user_profileMain"))
            
    else:
        flash(users_info)
        return redirect(url_for("user_profile.user_profileMain"))


@user_profile.route("/user-profile/remove-friend/<string:friend_name>", methods=["POST", "GET"])
@login_required
def remove_friend(friend_name):
    user = current_user

    result_01, users_info = user.get_usernames_and_user_id()
    if result_01:
        for user_info in users_info:
            if user_info["username"] == friend_name:
                friend_id = user_info["id"]
                break

        result_02, message = user.remove_friend(friend_id)
        flash(message)
        return redirect(url_for("user_profile.user_profileMain"))

    else:
        flash(users_info)
        return redirect(url_for("user_profile.user_profileMain"))
