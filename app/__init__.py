import os
from flask import Flask
from .models import db
from .auth import login_manager
from .auth.routes import page_not_found
from .routes import api
from .auth.routes import auth
from .spotify.routes import spot
from .yt.routes import yt

# This line shouldn't be used in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config.from_pyfile("config.py")
db.init_app(app)
app.register_error_handler(404, page_not_found)
app.register_blueprint(api)
app.register_blueprint(auth)
app.register_blueprint(spot)
app.register_blueprint(yt)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


