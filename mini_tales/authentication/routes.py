from flask import (flash, render_template,
                   redirect, request, session,
                   url_for, Blueprint)
from werkzeug.security import generate_password_hash, check_password_hash
from mini_tales import mongo

# Create a Blueprint authentication object 
authentication = Blueprint('authentication', __name__)

@authentication.route("/register", methods=["GET", "POST"])
def register():
    """
    This function registers an account for a user in the users database collection. 
    Once registered the user is taken to their My Tales page and a login session is created.
    The user is redirected back to the register page, if the username already exists or both
    password input fields do not match.
    The user's password is encrypted before storing in the users collection.
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("authentication.register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "liked_tales": []
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Account Successfully Created!")
        session["logged_in"] = True
        return redirect(url_for("tales.mytales", username=session["user"])) 
    return render_template("authentication/register.html")

@authentication.route("/login", methods=["GET", "POST"])
def login():
    """
    This function checks the user account exists and logs in the user if the username and password match.
    The user is redirected to the login page, if the username and/or password are incorrect.
    Once logged in the user is taken to their My Tales page and a login session is created.
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    session["logged_in"] = True
                    return redirect(url_for("tales.mytales", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("authentication.login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("authentication.login"))

    return render_template("authentication/login.html")

@authentication.route('/logout', methods=["GET","POST"])
def logout():
    """
    This function logs the user out of the site.
    The login session is removed and the user is 
    redirected to the login page.
    """
    session["logged_in"] = False
    session.clear()
    flash("Successfully Logged Out!")
    return render_template("authentication/login.html")