# Imports
import os
import sys
import time
import random
import tkinter
import pyrebase
import customtkinter
import tkinter.messagebox
# from dotenv import load_dotenv

# Firebase configuration
# load_dotenv('.env')

firebaseConfig = {
  "apiKey": "AIzaSyAE6LtDc1r7UizS5LHnPiNwnVsiprUuPk0",
  "authDomain": "coursework-e0974.firebaseapp.com",
  'databaseURL': "https://coursework-e0974-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "projectId": "coursework-e0974",
  "storageBucket": "coursework-e0974.appspot.com",
  "messagingSenderId": "726979196176",
  "appId": "1:726979196176:web:93a505c63cf66090186195",
  "measurementId": "G-BCJLPELCBE"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

e = 'ok@ok.ok'
p = 'okokok'
s = 'si'

if s == 'si':
    try:
        Login = auth.sign_in_with_email_and_password(e,p)
        print('S')
        print(Login)
        Login['displayName'] = 'Hello World!'
        print(Login)
    except:
        print('I')
else:
    try:
        Login = auth.create_user_with_email_and_password(e,p)
        print('S')
    except:
            print('I')

# Main app class
class App(customtkinter.CTk):

    # Initialisation
    def __init__(self):
        super().__init__()


    # Class methods
    ...

#
# Commented for now

# def main():
#     pass

# if __name__ == "__main__":
#     main()