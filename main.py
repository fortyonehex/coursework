# Imports
import os
import sys
import time
import random
import tkinter
import pyrebase
import sounddevice
import customtkinter
import tkinter.messagebox

#Firebase configuration

firebaseConfig = {
  'apiKey': "AIzaSyAE6LtDc1r7UizS5LHnPiNwnVsiprUuPk0",
  'authDomain': "coursework-e0974.firebaseapp.com",
  'databaseURL': "https://coursework-e0974-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "coursework-e0974",
  'storageBucket': "coursework-e0974.appspot.com",
  'messagingSenderId': "726979196176",
  'appId': "1:726979196176:web:93a505c63cf66090186195",
  'measurementId': "G-BCJLPELCBE"
}

firebase = pyrebase.initialize_app(firebaseConfig)

database = firebase.database()

storage = firebase.storage()

auth = firebase.auth()

while 1:
    e = input()
    p = input()
    s = input()

    if s == 'si':
        try:
            Login = auth.sign_in_with_email_and_password(e,p)
            print('S')
            print(Login)
            Login['displayName'] = Login['email'][:(Login['email'].find('@'))]
            database.child('users').child(Login['localId']).set({'email': Login['email'], 'displayName': Login['displayName']})
            storage.child(Login['localId']).put('/Users/kavinjayakumar/Desktop/S4-01 Timetable Term 1.png')
        except:
            print('I')
    else:
        try:
            Login = auth.create_user_with_email_and_password(e,p)
            print('S')
            print(Login)
            Login['displayName'] = Login['email'][:(Login['email'].find('@'))]
            database.child('users').child(Login['localId']).set({'email': Login['email'], 'displayName': Login['displayName']})
            storage.child(Login['localId']).put('/Users/kavinjayakumar/Desktop/S4-01 Timetable Term 1.png')
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