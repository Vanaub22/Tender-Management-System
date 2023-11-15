from tms import app,ma,db,mail
from flask import render_template,redirect,url_for,flash,request
from tms.models import Item,User
from flask import jsonify
from tms.models import Item,Bid
from tms.forms import RegisterForm,LoginForm,SellTenderForm,SetBidForm,ContactForm
from flask_login import login_user,logout_user,login_required,current_user
from flask_mail import Message
from datetime import datetime,timedelta

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been successfully logged out of your ProTender Account.",category='info')
    return redirect(url_for("home_page"))

# @app.route('/market/',methods=['GET','POST'])
# @login_required
# def market_page():
#     bid_form=SetBidForm()
#     sell_form=SellTenderForm()
#     if request.method=='POST':
#         # Set Bid Logic
#         bidding=request.form.get('bidding')
#         bid_obj=Item.query.filter_by(name=bidding).first()
#         if bid_obj:
#             if(current_user.can_set_bid(bid_obj)):
#                 bid_obj.bid(current_user)
#                 flash(f"Congratulations!! You have successfully set your bid for the {bid_obj.name} tender at ₹{bid_obj.price}", category='success')
#             else:
#                 flash("Unfortunately the bid cannot be made due to Insufficient Balance", category='danger')
#         # Selling Tender Logic
#         selling=request.form.get('selling')
#         sell_obj=Item.query.filter_by(name=selling).first()
#         if sell_obj:
#             if(current_user.can_sell(sell_obj)):
#                 sell_obj.sell(current_user)
#                 flash(f"Congratulations!! You have successfully let go of your bid for the {sell_obj.name} tender", category='success')
#             else:
#                 flash("Unfortunately you cannot let go of this bid because you are not holding it", category='danger')
#         return redirect(url_for('market_page'))
        
#     if request.method=='GET':        
#         items = Item.query.filter_by(owner=None)
#         owned_items=Item.query.filter_by(owner=current_user.id)
#         return render_template('market.html', items=items, bid_form=bid_form, owned_items=owned_items, sell_form=sell_form)
    
@app.route('/market/', methods=['GET', 'POST'])
@login_required
def market_page():
    bid_form = SetBidForm()
    sell_form = SellTenderForm()

    if request.method == 'POST':
        bidding = request.form.get('bidding')
        bid_obj = Item.query.filter_by(name=bidding).first()

        if bid_obj:
            if bid_obj.is_tender_open():  # Check if the tender is open
                amount = int(request.form.get('bid_amount'))  # Adjust to your form field name
                if(current_user.can_set_bid(bid_obj,amount)):
                    newBid=Bid()
                    newBid.amount=amount
                    newBid.bidder_id=current_user.id
                    newBid.tender_id=bid_obj.tid
                    if (bid_obj.price>=amount):
                        flash(f"The present value of the {bid_obj.name} tender is ₹{bid_obj.price}. Your Bid must be greater than the Present Valuation.",category='danger')
                    else:
                        prev_price=bid_obj.price
                        bid_obj.price=amount # price raised after bidding
                        bid_obj.bid(current_user,prev_price)
                        db.session.add(newBid)
                        db.session.commit()
                        flash(f"Congratulations!! You have successfully set your bid for the {bid_obj.name} tender at ₹{amount}", category='success')
                else:
                    flash("Unfortunately, the bid cannot be made due to Insufficient Balance or the tender is closed", category='danger')
            else:
                flash("Unfortunately, the tender is closed and no more bids can be placed.", category='danger')
        # Selling Tender Logic
        selling=request.form.get('selling')
        sell_obj=Item.query.filter_by(name=selling).first()
        if sell_obj:
            if(current_user.can_sell(sell_obj)):
                sell_obj.sell(current_user)
                flash(f"Congratulations!! You have successfully let go of your bid for the {sell_obj.name} tender", category='success')
            else:
                flash("Unfortunately you cannot let go of this bid because you are not holding it", category='danger')
        return redirect(url_for('market_page'))
    if request.method=='GET':        
        items = Item.query.all()
        owned_items=Item.query.filter_by(owner=current_user.id)
    return render_template('market.html', bid_form=bid_form, sell_form=sell_form, items=items)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,email_address=form.email_address.data,password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully. You are now logged in as {user_to_create.username}',category='success')
        return redirect(url_for('market_page'))
    if form.errors != {} : # no errors from the validation
        for err_msg in form.errors.values():
            flash(f'User Validation Error: {err_msg}',category='danger')
    return render_template('register.html',form=form)

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact_page():
    form = ContactForm()

    if form.validate_on_submit():
        user_email = current_user.email_address
        user_query = form.user_query.data
        tender_id = form.tender_id.data

        subject = f"Requesting Super-Admin privileges for Tender {tender_id} under ProTender Listing."
        body = f"User query: {user_query}\n\nTender ID: {tender_id}\nThis is an auto-generated mail. Please revert back to the request at {user_email}.\nProTender TMS."
        msg = Message(subject=subject, sender='webapptesting000@gmail.com', recipients=['anucbs2018@gmail.com'], body=body)
        mail.send(msg)

        flash('Your query has been submitted successfully! An email has been sent to the admins.', 'success')
        return redirect(url_for('contact_page'))
    
    return render_template('contact.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password do not Match! Please try again', category='danger')

    return render_template('login.html', form=form)

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'tid', 'desc', 'owner')

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# Route to handle JSON data and save it into the database
@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.json['name']
    price = request.json['price']
    tid = request.json['tid']
    desc = request.json['desc']
    new_item = Item(name=name, price=price, tid=tid, desc=desc)
    db.session.add(new_item)
    db.session.commit()
    return item_schema.jsonify(new_item)


# Route to delete a tender by its tender ID
@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    to_delete=Item.query.filter_by(id=item_id).first()
    # print(to_delete)
    if not to_delete:
        return jsonify({"Message":"Item not found"}),404
    item=to_delete
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Tender deleted successfully'})