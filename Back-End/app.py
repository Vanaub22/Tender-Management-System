from flask import Flask,session,render_template,request,redirect
import pyrebase

app=Flask(__name__)

config = {
  "apiKey": "AIzaSyAk3qSb4IxwQSKgKQj93IrF6upM2thIUp4",
  "authDomain": "protender-tms-system.firebaseapp.com",
  "projectId": "protender-tms-system",
  "storageBucket": "protender-tms-system.appspot.com",
  "messagingSenderId": "859770419080",
  "appId": "1:859770419080:web:3eaa43369e52df8ddeac3d",
  "measurementId": "G-DNL9EC460P",
  'databaseURL':""
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
app.secret_key='secret'

@app.route('/',methods=['POST','GET'])
def index():
    
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        try:
            user=auth.sign_in_with_email_and_password(email,password)
            session['user']=email
        except:
            return 'failed to login'
    return render_template("../Front-End/index.html")
@app.route('/logout')
def logout():
    pass

if __name__=='__main__':
    app.run(port=1111)
    