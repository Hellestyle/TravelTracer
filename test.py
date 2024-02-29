            user = User()
            success, message = user.registrer(firstName, lastName, email, username, password)
            if success:
                return f"{user}"
            else:
                flash(message)
                return redirect(url_for("sign_up"))