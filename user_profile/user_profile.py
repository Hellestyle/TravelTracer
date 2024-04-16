from forms import ChangePasswordForm, ChangeUsername, ChangePrivacySettings
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.user import User
from flask import flash
from database import Database

from models.wishlist import Wishlist
from models.visited_list import VisitedList
from models.achievement import Achievement

from config.application import POINTS_THRESHOLDS, ACHIEVEMENT_LEVEL_THRESHOLDS


user_profile = Blueprint("user_profile", __name__, template_folder="templates", static_folder="static")

@user_profile.route("/user-profile", methods=["POST", "GET"])
@user_profile.route("/user-profile/<int:user_id>")
def user_profileMain(user_id=None):
    
    if not current_user.is_authenticated and user_id is None:
        return redirect(url_for("reglog.login"))

    user = current_user if user_id is None else User().get_user_by_id(user_id)

    changePassForm = ChangePasswordForm()
    changeUserForm = ChangeUsername()
    changePrivacySettingsForm = ChangePrivacySettings()
    
    success, message, points = user.get_points()

    if not success:
        return message

    points_level = None

    for threshold, level in POINTS_THRESHOLDS.items():
        if points >= threshold:
            points_level = level
        else:
            break

    with Database(dict_cursor=True) as db:

        wishlist_model = Wishlist(db)
        visited_list_model = VisitedList(db)
        achievement_model = Achievement(db)

        success, message, wishlist = wishlist_model.getWishlist(user.get_id())

        if not success:
            return message
        
        success, message, visited_list = visited_list_model.getVisitedList(user.get_id())

        if not success:
            return message

        success, message, achievements = achievement_model.getAchievements()

        if not success:
            return message
        
        success, message, user_achievements_db = achievement_model.getUserAchievements(user.get_id())

        if not success:
            return message
        
        user_achievements = {}

        for achievement_id, count in user_achievements_db.items():

            current_level = None

            for threshold, level in ACHIEVEMENT_LEVEL_THRESHOLDS.items():
                if count >= threshold:
                    current_level = level
                else:
                    break

            user_achievements[achievement_id] = {
                "count": count,
                "level": current_level
            }
    
    #Denne må være her for å sende inn info etter man har endret pass,navn eller personvern innstillinger
    result_01, user_info = user.get_user_info()
    result_02, friend_amount = user.get_friend_amount()
    result_03, friend_list = user.get_friendlist()
    result_04, friend_requests = user.get_friend_requests()
    result_05, sent_requests = user.show_sent_friend_request()

    admin = False
    is_friend = False
    check_sent_request = False
    if current_user.is_authenticated:
        user = current_user
        admin = True if user.check_if_user_is_admin() else False
        
        if user.is_friend(user_id):
            is_friend = True

        if user.get_id() != user_id:
            result = user.check_sent_friend_request(user_id)
            if result:
                check_sent_request = True
    

    if request.method == "GET":
        changeUserForm.newUsername.data = user.getUsername()

        if result_01 and result_02 and result_03 and result_04 and result_05:
            return render_template("user_profile/user_profile.html",
                                user_id=user_id, user=user,
                                changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                user_info=user_info, friend_amount=friend_amount, \
                                friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm,
                                points=points, points_level=points_level,
                                achievements=achievements, user_achievements=user_achievements,
                                wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests,
                                admin=admin, is_friend=is_friend, check_sent_request=check_sent_request
                            )
        else:
            if result_01 is False:
                flash(user_info)
            elif result_02 is False:
                flash(friend_amount)
            elif result_03 is False:
                flash(friend_list)
            elif result_04 is False:
                flash(friend_requests)
            else:
                flash(sent_requests)
            return render_template("user_profile/user_profile.html",
                                user_id=user_id, user=user,
                                changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                user_info=user_info, friend_amount=friend_amount, \
                                friend_list=friend_list, friend_requests=friend_requests,changePrivacySettingsForm=changePrivacySettingsForm,
                                points=points, points_level=points_level,
                                achievements=achievements, user_achievements=user_achievements,
                                wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests,
                                admin=admin, is_friend=is_friend, check_sent_request=check_sent_request
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
                flash(message, category = "success")
                return render_template("user_profile/user_profile.html",
                                    user_id=user_id, user=user,
                                    changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                    user_info=user_info, friend_amount=friend_amount,
                                    friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm,
                                    points=points, points_level=points_level,
                                    achievements=achievements, user_achievements=user_achievements,
                                    wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests,
                                    admin=admin
                                )
            else:
                flash(message, category = "error")
                return render_template("user_profile/user_profile.html",
                                    user_id=user_id, user=user,
                                    changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                    user_info=user_info, friend_amount=friend_amount,
                                    friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm,
                                    points=points, points_level=points_level,
                                    achievements=achievements, user_achievements=user_achievements,
                                    wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests,
                                    admin=admin
                                )
            

        elif changeUserForm.submitUsernameChange.data and changeUserForm.validate():
            # Username and Name change 
            newUsername = changeUserForm.newUsername.data
            password = changeUserForm.password.data
            newFirstName = changeUserForm.newFirstName.data
            newLastName = changeUserForm.newLastName.data
            
            user = current_user
            success, message = user.changeNames(password,newUsername,newFirstName,newLastName)
            if success:
                user_info["username"] = newUsername
                user_info["first_name"] = newFirstName
                user_info["last_name"] = newLastName
                current_user.update()
                message = "Succesfully changed User names !"
                flash(message, category = "success")
                return render_template("user_profile/user_profile.html",
                                    user_id=user_id, user=user,
                                    changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                    user_info=user_info, friend_amount=friend_amount,
                                    friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm,
                                    points=points, points_level=points_level,
                                    achievements=achievements, user_achievements=user_achievements,
                                    wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests,
                                    admin=admin
                                )
            else:
                flash(message, category = "error")
                return render_template("user_profile/user_profile.html",
                                    user_id=user_id, user=user,
                                    changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                    user_info=user_info, friend_amount=friend_amount,
                                    friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm,
                                    points=points, points_level=points_level,
                                    achievements=achievements, user_achievements=user_achievements,
                                    wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests,
                                    admin=admin
                                )
            

        
        elif changePrivacySettingsForm.submitPrivacySettings.data and changePrivacySettingsForm.validate():
            # Privacy settings change
            success, message = user.updatePrivacySettings( changePrivacySettingsForm.openProfile.data,changePrivacySettingsForm.showFriendslist.data,changePrivacySettingsForm.showRealName.data)
            if success:
                user_info["open_profile"] = changePrivacySettingsForm.openProfile.data
                user_info["show_friendslist"] = changePrivacySettingsForm.showFriendslist.data
                user_info["show_real_name"] = changePrivacySettingsForm.showRealName.data
                current_user.update()
                message = "Succesfully changed privacy settings !"
                flash(message, category = "success")
                return render_template("user_profile/user_profile.html",
                                    user_id=user_id, user=user,
                                    changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                    user_info=user_info, friend_amount=friend_amount,
                                    friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm,
                                    points=points, points_level=points_level,
                                    achievements=achievements, user_achievements=user_achievements,
                                    wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests,
                                    admin=admin
                                )
            else:
                flash(message, category = "error")
                return render_template("user_profile/user_profile.html",
                                    user_id=user_id, user=user,
                                    changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                    user_info=user_info, friend_amount=friend_amount,
                                    friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm,
                                    points=points, points_level=points_level,
                                    achievements=achievements, user_achievements=user_achievements,
                                    wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests,
                                    admin=admin
                                )
            
        
        # Error handling
        else:
            if changePassForm.errors:
                for errors in changePassForm.errors.values():
                    for error in errors:
                        flash(error, category = "error")
            elif changeUserForm.errors:
                for errors in changeUserForm.errors.values():
                    for error in errors:
                        flash(error, category = "error")
            else:
                for errors in changePrivacySettingsForm.errors.values():
                    for error in errors:
                        flash(error, category = "error")
            return render_template("user_profile/user_profile.html",
                                user_id=user_id, user=user,
                                changePassForm=changePassForm, changeUserForm=changeUserForm, \
                                friend_list=friend_list, friend_requests=friend_requests, changePrivacySettingsForm=changePrivacySettingsForm, user_info=user_info, friend_amount=friend_amount,
                                points=points, points_level=points_level,
                                achievements=achievements, user_achievements=user_achievements,
                                wishlist=wishlist, visited_list=visited_list, sent_requests=sent_requests, admin=admin
                            )


@user_profile.route("/user-profile/accept-friend-request/<string:sender_name>", methods=["POST", "GET"])
@login_required
def accept_friend_request(sender_name):
    user = current_user

    result_01, users_info = user.get_usernames_and_user_id()
    if result_01:
        sender_id = None
        for user_info in users_info:
            if user_info["username"] == sender_name:
                sender_id = user_info["id"]
                break

        result_02, message = user.accept_friend_request(sender_id)
        flash(message, category = "success")
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
        sender_id = None
        for user_info in users_info:
            if user_info["username"] == sender_name:
                sender_id = user_info["id"]
                break
        
        result_02, message = user.decline_friend_request(sender_id)
        flash(message, category = "error")
        return redirect(url_for("user_profile.user_profileMain"))
            
    else:
        flash(users_info)
        return redirect(url_for("user_profile.user_profileMain"))


@user_profile.route("/user-profile/send-friend-request/<string:receiver_name>", methods=["POST", "GET"])
@login_required
def send_friend_request(receiver_name):
    user = current_user

    result_01, users_info = user.get_usernames_and_user_id()
    if result_01:
        receiver_id = None
        for user_info in users_info:
            if user_info["username"] == receiver_name:
                receiver_id = user_info["id"]
                break

        if receiver_id:
            result_02, message = user.send_friend_request(receiver_id)
            flash(message, category = "success")
            return redirect(url_for("user_profile.user_profileMain"))
        else:
            flash("User not found", category = "error")
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
        friend_id = None
        for user_info in users_info:
            if user_info["username"] == friend_name:
                friend_id = user_info["id"]
                break
        
        result_02, message = user.remove_friend(friend_id)
        flash(message, category = "error")
        return redirect(url_for("user_profile.user_profileMain"))

    else:
        flash(users_info)
        return redirect(url_for("user_profile.user_profileMain"))
    

@user_profile.route("/user-profile/cancel-friend-request/<string:receiver_name>", methods=["POST", "GET"])
@login_required
def cancel_friend_request(receiver_name):
    user = current_user

    result_01, users_info = user.get_usernames_and_user_id()
    if result_01:
        receiver_id = None
        for user_info in users_info:
            if user_info["username"] == receiver_name:
                receiver_id = user_info["id"]
                break

        if receiver_id:
            result_02, message = user.cancel_friend_request(receiver_id)
            flash(message)
            return redirect(url_for("user_profile.user_profileMain"))
    else:
        flash(users_info)
        return redirect(url_for("user_profile.user_profileMain"))
