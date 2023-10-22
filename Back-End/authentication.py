import pyrebase

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

firebase=pyrebase.initialize_app(config);
auth=firebase.auth()

email="test@gmail.com"
password="123456"

# user=auth.create_user_with_email_and_password(email,password)
# print(user)
user=auth.sign_in_with_email_and_password(email,password)
# info=auth.get_account_info(user['idToken'])
# print(info)
# auth.send_email_verification(user['idToken'])
auth.send_password_reset_email(email)