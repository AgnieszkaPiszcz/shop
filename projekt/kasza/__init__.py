from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '074d6c3d31585cd60d7dcd92b365494f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_maganer = LoginManager(app)
login_maganer.login_view = 'login'
login_maganer.login_message_category = 'info'

from kasza import routes

