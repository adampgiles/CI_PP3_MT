import os
from datetime import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")

@app.route("/get_tales", methods=["GET","POST"])
def get_tales():    
    tales = mongo.db.tales.find()
    if session.get("logged_in") == True:
        liked = mongo.db.users.find_one({"username": session["user"]})["liked_tales"]
        session["liked"] = liked
    if request.method == "POST":
        search = request.form.get("search-input")
        tales = mongo.db.tales.find({"tale_title": {"$regex": str(search), "$options" :'i'}})
        return render_template("tales.html", tales=tales)
    return render_template("tales.html", tales=tales)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "liked_tales": []
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        session["logged_in"] = True
        return redirect(url_for("mytales", username=session["user"]))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    session["logged_in"] = True
                    return redirect(url_for("mytales", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/logout', methods=["GET","POST"])
def logout():
    session["logged_in"] = False
    session.clear()
    flash("Successfully Logged Out!")
    return render_template("login.html")

@app.route("/mytales/<username>", methods=["GET","POST"])
def mytales(username):
    username = mongo.db.users.find_one({"username": session["user"]})["username"]
    tales = mongo.db.tales.find({"tale_author": session["user"]})    
    return render_template("mytales.html", username=username, tales=tales)

@app.route("/newtale", methods=["GET", "POST"])
def newtale():
    date = datetime.now()
    if request.method == "POST":
        usertale = {
            "tale_title": request.form.get("title"),
            "tale_blurb": request.form.get("blurb"),
            "tale_topic": request.form.get("topic"),
            "tale_content": request.form.get("tale-content"),
            "tale_likes": 0,
            "tale_views": 0,
            "tale_publish_date": date.strftime("%d/%m/%Y"),
            "tale_author": session["user"]
        }
        mongo.db.tales.insert_one(usertale)
        flash("Tale Shared Successfully!")
        return redirect(url_for("mytales", username=session["user"]))
    return render_template("newtale.html") 

@app.route("/edittale/<_id>", methods=["GET","POST"])
def edittale(_id): 
    date = datetime.now()
    _id = _id
    tale = mongo.db.tales.find_one({"_id": ObjectId(_id)})
    if request.method == "POST":
        mongo.db.tales.update_one(
            {"_id": ObjectId(_id)},
            { "$set": {
            "tale_title": request.form.get("title"),
            "tale_blurb": request.form.get("blurb"),
            "tale_topic": request.form.get("topic"),
            "tale_content": request.form.get("tale-content"),
            "tale_likes": 0,
            "tale_views": 0,
            "tale_publish_date": date.strftime("%d/%m/%Y")
            }})
        mongo.db.users.update_many({"liked_tales": _id},{ "$pull": {"liked_tales": _id}})
        flash("Tale Edited Successfully!")
        return redirect(url_for("mytales", username=session["user"]))
    return render_template("edittale.html", _id=_id, tale=tale)   

@app.route("/deletetale/<_id>", methods=["GET","POST"])
def deletetale(_id):
    _id = _id
    tale = mongo.db.tales.find_one({"_id": ObjectId(_id)}) 
    return render_template("deletetale.html", _id=_id, tale=tale) 

@app.route("/confirmdeletetale/<_id>", methods=["GET","POST"])
def confirmdeletetale(_id): 
    _id = _id
    mongo.db.tales.delete_one({"_id": ObjectId(_id)})
    mongo.db.users.update_many({"liked_tales": _id},{ "$pull": {"liked_tales": _id}})
    flash("Tale Deleted Successfully!")
    return redirect(url_for("mytales", username=session["user"]))   

@app.route("/tale/<_id>", methods=["GET","POST"])
def tale(_id):    
    _id = _id
    mongo.db.tales.update_one({"_id": ObjectId(_id)},{ "$inc": {"tale_views": 1}})
    tale = mongo.db.tales.find_one({"_id": ObjectId(_id)}) 
    if session.get("logged_in") == True: 
        liked = mongo.db.users.find_one({"username": session["user"]})["liked_tales"]
        session["liked"] = liked
    return render_template("tale.html", _id=_id, tale=tale)

@app.route("/like_tale/<_id>", methods=["GET","POST"])
def like_tale(_id): 
    _id = _id
    liked = mongo.db.users.find_one({"username": session["user"]})["liked_tales"]
    if _id in liked:
        mongo.db.users.update_one({"username": session["user"]},{ "$pull": {"liked_tales": _id}})
        mongo.db.tales.update_one({"_id": ObjectId(_id)},{ "$inc": {"tale_likes": -1}})        
    else:
        mongo.db.users.update_one({"username": session["user"]},{ "$push": {"liked_tales": _id}})
        mongo.db.tales.update_one({"_id": ObjectId(_id)},{ "$inc": {"tale_likes": 1}})
    liked = mongo.db.users.find_one({"username": session["user"]})["liked_tales"]
    session["liked"] = liked
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
            
