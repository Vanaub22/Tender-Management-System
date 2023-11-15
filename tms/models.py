from tms import db,bcrypt,login_manager
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000000)
    owned_items = db.relationship('Item', backref='owned_user', lazy=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_set_bid(self,t,amt):
        if(self.id==t.owner):
            return self.budget>=(amt-t.price)
        else:
            return self.budget>=amt
    
    def can_sell(self,s):
        return s in self.owned_items
    

class Item(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=60),nullable=False,unique=True)
    price=db.Column(db.Integer(),nullable=False)
    tid=db.Column(db.String(length=12),nullable=False,unique=True)
    desc=db.Column(db.String(length=2000),nullable=False,unique=True)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))
    bids = db.relationship('Bid', backref='tender', lazy=True)
    closing_date = db.Column(db.DateTime)



    def __repr__(self):
        return f"Tender {self.tid}"
    
    def bid(self,user,prev_price):
        if(self.owner==None):
            self.owner=user.id
            user.budget-=self.price
        elif(self.owner==user.id): # if the same bidder is bidding again
            # price has already been assigned to the new bid
            user.budget-=(self.price-prev_price)
        else:
            owner_id=self.owner
            prev_user=User.query.get(owner_id)
            prev_user.budget+=self.price
            self.owner=user.id
            user.budget-=self.price
        db.session.commit()

    def sell(self,user):
        self.owner=None
        user.budget+=self.price
        db.session.commit()
        
    def is_tender_open(self):
        return datetime.datetime.utcnow() < self.closing_date
    
    

class Bid(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Integer(), nullable=False)
    bidder_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    tender_id = db.Column(db.Integer(), db.ForeignKey('item.id'), nullable=False)

    def bid(self, user, amount):
        if not self.is_tender_open():
            return False  # Tender is closed
        if user.can_set_bid(amount):
            bid = Bid(amount=amount, bidder_id=user.id, tender_id=self.id)
            db.session.add(bid)
            db.session.commit()
            return True
        else:
            return False  # User doesn't have enough budget
    
    def is_tender_open(self):
        return datetime.datetime.utcnow() < self.closing_date
    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_key =db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))