from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,TextAreaField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError,NumberRange
from tms.models import User
class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!! Try a different Username')
        
    def validate_email_address(self,email_address_to_check):
        email_address=User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists!! Try a different e-mail address')
    username=StringField(label="Enter Username:",validators=[Length(min=2),DataRequired()])
    email_address=StringField(label="Enter E-mail Address:",validators=[Email(),DataRequired()])
    password1=PasswordField(label="Enter Password:",validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label="Confirm Password:",validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label="Create Account")

class LoginForm(FlaskForm):
    username = StringField(label='Enter Username:', validators=[DataRequired()])
    password = PasswordField(label='Enter Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class SetBidForm(FlaskForm):
    bid_amount = IntegerField(label="Enter Bidding Amount:", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField(label='Set Bid for Tender')

class ContactForm(FlaskForm):
    user_query = TextAreaField('Your Query', validators=[DataRequired()])
    tender_id = StringField('Tender ID in Discussion')
    submit = SubmitField('Submit')

class SellTenderForm(FlaskForm):
    submit = SubmitField(label='Sell Tender')