from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
app = Flask(__name__)
ma = Marshmallow(app) 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tms.db'
app.config['SECRET_KEY']='E39058C761AB'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"
from tms import routes
