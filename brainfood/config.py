import os
import connexion

from database import db_session

basedir = os.path.abspath(os.path.dirname(__file__))

db = db_session

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
