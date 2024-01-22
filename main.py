# Imports
import sys
import time
import random
import tkinter
import pyrebase
import customtkinter
import tkinter.messagebox

# Firebase configuration
config = {
  "apiKey": "AIzaSyAE6LtDc1r7UizS5LHnPiNwnVsiprUuPk0",
  "authDomain": "coursework-e0974.firebaseapp.com",
  "projectId": "coursework-e0974",
  "storageBucket": "coursework-e0974.appspot.com",
  "messagingSenderId": "726979196176",
  "appId": "1:726979196176:web:93a505c63cf66090186195",
  "measurementId": "G-BCJLPELCBE"
}

firebase = pyrebase.initialize_app(config)

try:
    IsUser=user['userId']
except:
       IsUser = None

auth = firebase.auth()

# Main app class
class App(customtkinter.CTk):

    # Initialisation
    def __init__(self):
        super().__init__()
        

    # Class methods
    ...


# Commented for now

# def main():
#     pass

# if __name__ == "__main__":
#     main()
