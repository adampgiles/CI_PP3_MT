import os
from flask import (Flask, render_template)
from flask_pymongo import PyMongo

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
mongo.init_app(app)


def page_not_found(e):
    return render_template('404.html'), 404


def create_app():
    """
    Creates an app with the authentication and tales blueprint routes
    """
    # Import the routes
    from mini_tales.authentication.routes import authentication
    from mini_tales.tales.routes import tales
    # Register the routes with the app
    app.register_blueprint(authentication)
    app.register_blueprint(tales)
    # Register 404 error page
    app.register_error_handler(404, page_not_found)
    # Return the app
    return app
