from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_login import LoginManager
from werkzeug.utils import secure_filename


def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname( __file__ ),p))

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)
IMG_FOLDER = os.path.join('static', 'images')
app.config["UPLOAD_FOLDER"] = IMG_FOLDER
Flask_Logo = os.path.join(app.config["UPLOAD_FOLDER"], "sortie1.jpg")
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.sqlite'))
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "7d49295c-541c-4db7-8e5a-230a49389189"

login_manager = LoginManager(app)
login_manager.login_view = "login"


