from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os



file_path = os.path.abspath(os.getcwd())+"/site.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_maganer = LoginManager(app)
login_maganer.login_view = 'login'
login_maganer.login_message_category = 'info'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from shop import routes
from shop import models

