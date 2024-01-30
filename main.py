# Imports
import os
import sys
import time
import random
import tkinter
import pyrebase
import sounddevice
import customtkinter

#Firebase configuration

    # Retrieving configuration keys

with open('.env', 'r') as env:
    firebaseConfig = exec(''.join(env.readlines()))

firebase = pyrebase.initialize_app(firebaseConfig)

database = firebase.database()

storage = firebase.storage()

auth = firebase.auth()

while 1:
    e = input()
    p = input()
    s = input()

    if e or p or s == 'q':
        break

    if s == 'si':
        try:
            Login = auth.sign_in_with_email_and_password(e,p)
            print('S')
            print(Login)
            Login['displayName'] = Login['email'][:(Login['email'].find('@'))]
            database.child('users').child(Login['localId']).set({'email': Login['email'], 'displayName': Login['displayName']})
            storage.child(Login['displayName']).put('/Users/kavinjayakumar/Desktop/S4-01 Timetable Term 1.png')
        except:
            print('I')
    else:
        try:
            Login = auth.create_user_with_email_and_password(e,p)
            print('S')
            print(Login)
            Login['displayName'] = Login['email'][:(Login['email'].find('@'))]
            database.child('users').child(Login['localId']).set({'email': Login['email'], 'displayName': Login['displayName']})
            storage.child(Login['displayName']).put('/Users/kavinjayakumar/Desktop/S4-01 Timetable Term 1.png')
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