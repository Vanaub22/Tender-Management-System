from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_mail import Mail

admin = Admin()
app = Flask(__name__)
admin.init_app(app)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tms.db'
app.config['SECRET_KEY'] = 'E39058C761AB'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'webapptesting000@gmail.com'
app.config['MAIL_PASSWORD'] = 'axsr gtnh qini mhoa'
app.config['MAIL_DEFAULT_SENDER'] = 'webapptesting000@gmail.com'
mail=Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from tms import routes  # Using Lazy importing to avoid circular imports
from tms.models import User, Item, Bid  # Using Lazy importing to avoid circular imports

class UserView(ModelView):
    can_view_details = True

class ItemView(ModelView):
    can_view_details = True

class BidView(ModelView):
    can_view_details = True

admin.add_view(UserView(User, db.session))
admin.add_view(ItemView(Item, db.session))
admin.add_view(BidView(Bid, db.session))