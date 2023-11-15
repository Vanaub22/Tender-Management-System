from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_mail import Mail
from flask import redirect,url_for,request,flash
from flask_login import current_user,login_user,login_required

app = Flask(__name__)
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
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from tms import routes,models # Using Lazy importing to avoid circular imports
# from tms.models import User, Item, Bid, Admin
from flask_admin import Admin,AdminIndexView,expose
class MyAdminIndexView(AdminIndexView):
        def is_visible(self):
            return False
        @expose('/')
        @login_required
        def index(self):
            if not current_user.is_authenticated:
                return redirect(url_for('.admin_login'))
            return super(MyAdminIndexView,self).index()
        @expose('/admin-login/', methods=['GET', 'POST'])
        def admin_login(self):
            if request.method == 'POST':
                admin_key = request.form.get('admin_key')
                password = request.form.get('password')
                # Check if the entered admin key and password are correct
                admin = models.Admin.query.filter_by(admin_key=admin_key, password=password).first()
                if admin:
                    login_user(admin)
                    flash(f'You are now inside the Super Admin Portal',category='success')
                    # return self.render(url_for('.index'))
                    return redirect(url_for('.index'))
                    # return super(MyAdminIndexView,self).index()
            flash(f'You are not allowed to access the Admin portal',category='danger')
            return self.render('admin/admin-login.html',user=current_user)

admin = Admin(index_view=MyAdminIndexView())
admin.init_app(app)

class UserView(ModelView):
    can_view_details = True

class ItemView(ModelView):
    can_view_details = True

class BidView(ModelView):
    can_view_details = True

admin.add_view(UserView(models.User, db.session))
admin.add_view(ItemView(models.Item, db.session))
admin.add_view(BidView(models.Bid, db.session))