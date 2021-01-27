"""
Main module of the server file
"""
import os
import connexion

# 3rd party moudles
from flask import render_template

# local modules
from database import init_db

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


if __name__ == "__main__":
    init_db()
    connex_app.run(debug=True)
