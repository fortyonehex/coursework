# Imports
import os
import sys
import time
import base64
import random
import tkinter
import pyrebase
import sounddevice
import customtkinter
from PIL import Image
from dotenv import load_dotenv

# Firebase configuration

## Retrieving configuration keys
load_dotenv('.env')

firebaseConfig = eval(os.getenv('CONFIG'))

firebase = pyrebase.initialize_app(firebaseConfig)

print('Initialised')

database = firebase.database()

storage = firebase.storage()

auth = firebase.auth()

while 1:
    e = input('e: ')
    p = input('p: ')
    s = input('s: ')

    if (e or p or s) == 'q':
        break

    if s == 'si':
        try:
            user = auth.sign_in_with_email_and_password(e,p)
            print('S')
            print(user)
            user = database.child('users').child(user['localId'])
            print('Here')
            print(user['expiresIn'])
            time.sleep(5)
            print(user['expiresIn'])
            print('Here')
            print('\n\n' + storage.bucket.get_blob(user.child('displayName')).download_as_string())
        except:
            print('I')
    elif s == 'su':
        try:
            user = auth.create_user_with_email_and_password(e,p)
            print('S')
            user['displayName'] = user['email'][:(user['email'].find('@'))]
            print('D')
            database.child(f"users/{user['localId']}").set(user)
            print('E')
            storage.child('images/E').upload('EnviroMate Icon copy.png')
            print('F')
            print(storage.child('E').get_url(None))
        except:
            print('I')
    else:
        print('\nTRY AGAIN\n')

print('Exited')

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