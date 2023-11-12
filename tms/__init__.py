from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from tms.models import User,Item
admin=Admin()
app = Flask(__name__)
admin.init_app(app)
ma = Marshmallow(app) 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tms.db'
app.config['SECRET_KEY']='E39058C761AB'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"
from tms import routes

class UserView(ModelView):
    can_view_details=True

class ItemView(ModelView):
    can_view_details=True

from tms.models import User,Item # Using Lazy importing to avoid circular imports
admin.add_view(UserView(User,db.session))
admin.add_view(ItemView(Item,db.session))