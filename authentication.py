import pickle
import pyrebase
import firebase_admin
from firebase_admin import *
from firebase_admin import auth as firebase_auth
from dotenv import load_dotenv

# Retrieving configuration keys

load_dotenv('.env')

firebaseConfig = eval(os.getenv('CONFIG'))
cred = credentials.Certificate("service_account.json")

firebase_admin.initialize_app(cred)
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database = firebase.database()


def create_user(email, password, motherTongue, level):
    try:
        print('CR')
        user = dict(auth.create_user_with_email_and_password(email, password))
        user['displayName'] = user['email'][:(user['email'].find('@'))]
        print('SETTING')
        database.child(f"users/{user['localId']}").set({
            'idToken': user['idToken'],
            'display_name': user['displayName'],
            'email': email,
            'mother_tongue': motherTongue,
            'level': level,
            'ability_quiz_tries': 0,
            'ability_quiz_score': 0,
            'targeted_practice_level': 0,
            'targeted_practice_tries': 0,
        })
        print('SET')
        return user['idToken']
    except:
        return None


# def reset_password(email):
#     try:
#         auth.send_password_reset_email(email)
#         return not None
#     except:
#         return None


def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user['idToken']
    except:
        return None


def store_session(token):
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')
    with open('token.pickle', 'wb') as f:
        pickle.dump(token, f)


def load_token():
    try:
        with open('token.pickle', 'rb') as f:
            token = pickle.load(f)
        # print(token)
        return token
    except:
        return None

def load_user():
    print("STARTs")
    try:
        print(authenticate_token(load_token()))
        info = database.child(f"users/{authenticate_token(load_token())}").get()
        print('D 1')
        user = info.val()
        print('D 2')
        print(user)
        print(info)
        return user
    except:
        print('FAIL')
        return None

def authenticate_token(token):
    try:
        result = firebase_auth.verify_id_token(token)
        return result['user_id']
    except:
        return None


def get_name(token):
    try:
        result = firebase_auth.verify_id_token(token)
        return result['name']
    except:
        return None


def revoke_token(token):
    result = firebase_auth.revoke_refresh_tokens(authenticate_token(token))
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')