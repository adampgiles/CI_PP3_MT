from datetime import datetime
from flask import (flash, render_template,
    redirect, request, session, url_for, Blueprint)
from bson.objectid import ObjectId
from mini_tales import mongo

# Create a Blueprint authentication object 
tales = Blueprint('tales', __name__)

@tales.route("/")
@tales.route("/get_tales", methods=["GET","POST"])
def get_tales():    
    """
    This function displays all tales in the tales collection on the base template.
    """  
    if session.get("search") != None:
        search = session.get("search")         
        if search == "":
            session["search"] = search
            tales = mongo.db.tales.find()
        else:            
            session["search"] = search
            tales = mongo.db.tales.find({"$text": { "$search": search }})
    else:
        session["search"] = ""
        tales = mongo.db.tales.find()
        
    if request.method == "POST":         
        search = request.form.get("search-input") 
        print(search) 
        if search == "":
            session["search"] = search
            tales = mongo.db.tales.find()
        else:            
            tales = mongo.db.tales.find({"$text": { "$search": str(search) }})
            session["search"] = search
        return render_template("tales/tales.html", tales=tales) 
        
    if session.get("logged_in") == True:
        liked = mongo.db.users.find_one({"username": session["user"]})["liked_tales"]
        session["liked"] = liked
        session["fulltale"] = False     

    return render_template("tales/tales.html", tales=tales)

@tales.route("/clear_search", methods=["POST"])
def clear_search():
    session["search"] = ""
    tales = mongo.db.tales.find()
    return render_template("tales/tales.html", tales=tales)

@tales.route("/mytales/<username>", methods=["GET","POST"])
def mytales(username):
    """
    This function displays all of the currently logged in user's tales in the tales collection on the base template.
    """
    username = mongo.db.users.find_one({"username": session["user"]})["username"]
    tales = mongo.db.tales.find({"tale_author": session["user"]})    
    return render_template("tales/mytales.html", username=username, tales=tales)

@tales.route("/newtale", methods=["GET", "POST"])
def newtale():
    """
    This function displays a form that the user can use to submit a new tale to
    the tales collection.
    The user is redirected to their My Tales page, once submitted. 
    """
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
        return redirect(url_for("tales.mytales", username=session["user"]))
    return render_template("tales/newtale.html") 

@tales.route("/edittale/<_id>", methods=["GET","POST"])
def edittale(_id): 
    """
    This function displays a pre-populated form that the user can use to edit one of their existing tales.
    Changes will then update the existing tales collection document.
    The user is redirected to their My Tales page, once changes are submitted. 
    """
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
        return redirect(url_for("tales.mytales", username=session["user"]))
    return render_template("tales/edittale.html", _id=_id, tale=tale)   

@tales.route("/deletetale/<_id>", methods=["GET","POST"])
def deletetale(_id):
    """
    This function takes the user to a page where they can confirm if 
    they are sure about deleting their existing tale.    
    """
    _id = _id
    tale = mongo.db.tales.find_one({"_id": ObjectId(_id)}) 
    return render_template("tales/deletetale.html", _id=_id, tale=tale) 

@tales.route("/confirmdeletetale/<_id>", methods=["GET","POST"])
def confirmdeletetale(_id): 
    """
    This function deletes the user's existing tale,
    removing the document from the collection.
    The user is redirected to their My Tales page, once this change is actioned. 
    """
    _id = _id
    mongo.db.tales.delete_one({"_id": ObjectId(_id)})
    mongo.db.users.update_many({"liked_tales": _id},{ "$pull": {"liked_tales": _id}})
    flash("Tale Deleted Successfully!")
    return redirect(url_for("tales.mytales", username=session["user"]))   

@tales.route("/tale/<_id>", methods=["GET","POST"])
def tale(_id): 
    """
    This function displays the full tale that was selected on the tales page.
    """   
    _id = _id
    mongo.db.tales.update_one({"_id": ObjectId(_id)},{ "$inc": {"tale_views": 1}})
    tale = mongo.db.tales.find_one({"_id": ObjectId(_id)}) 
    if session.get("logged_in") == True: 
        liked = mongo.db.users.find_one({"username": session["user"]})["liked_tales"]
        session["liked"] = liked
        session["fulltale"] = True
    return render_template("tales/tale.html", _id=_id, tale=tale)

@tales.route("/like_tale/<_id>", methods=["GET","POST"])
def like_tale(_id): 
    """
    This function allows the logged in user to increase/decrease
    a tale's like count by a factor of 1. The tale's id is stored 
    in the current user's collection document, to ensure the user can only
    like a tale once.
    """ 
    _id = _id
    liked = mongo.db.users.find_one({"username": session["user"]})["liked_tales"]
    if _id in liked:
        mongo.db.users.update_one({"username": session["user"]},{ "$pull": {"liked_tales": _id}})
        mongo.db.tales.update_one({"_id": ObjectId(_id)},{ "$inc": {"tale_likes": -1}})
        if session.get("fulltale") == True:  
            mongo.db.tales.update_one({"_id": ObjectId(_id)},{ "$inc": {"tale_views": -1}})      
    else:
        mongo.db.users.update_one({"username": session["user"]},{ "$push": {"liked_tales": _id}})
        mongo.db.tales.update_one({"_id": ObjectId(_id)},{ "$inc": {"tale_likes": 1}})
        if session.get("fulltale") == True:  
            mongo.db.tales.update_one({"_id": ObjectId(_id)},{ "$inc": {"tale_views": -1}}) 
    liked = mongo.db.users.find_one({"username": session["user"]})["liked_tales"]
    session["liked"] = liked
    return redirect(request.referrer)