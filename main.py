# Imports
import os
import re
import sys
import flet
import time
import base64
import pickle
import random
import asyncio
import pyrebase
import authentication
import urllib.request
from dotenv import load_dotenv

# Retrieving configuration keys

load_dotenv('.env')

firebaseConfig = eval(os.getenv('CONFIG'))

# Check internet access

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)

        # Firebase configuration

        global firebase
        firebase = pyrebase.initialize_app(firebaseConfig)
        global database
        database = firebase.database()
        global storage
        storage = firebase.storage()
        global auth
        auth = firebase.auth()

        return True
    except:
        return False

connect()

user = {}

# Colour codes

PRIMARY = '#8AB1D0'
SECONDARY = '#0D1931'
TERTIARY = '#8D887C'
ACCENT = '#DD4055'
BG = '#F2EFE9'
TEXT = '#2E2F2F'

# Main app class

class Main(flet.UserControl):
    def __init__(self, page: flet.Page):
        super().__init__()
        self.page = page
        self.init()
        print(page.views,"\n\n\n")
        page.title = "Unolingo"
        page.theme_mode = "light"
        page.window_width = 1440
        page.window_min_width = 1200
        page.window_height = 800
        page.window_min_height = 750
        page.window_resizable = True
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.MainAxisAlignment.CENTER

        theme = flet.Theme()
        theme.page_transitions.macos = flet.PageTransitionTheme.NONE
        page.theme = theme
        page.update()

        # self.ICBanner = flet.Banner(
        #     bgcolor=flet.colors.AMBER_100,
        #     leading=flet.Icon(flet.icons.WARNING_AMBER_ROUNDED, color=flet.colors.AMBER, size=40),
        #     content=flet.Text(
        #         "Oops, it seems like you are not connected to the internet.",
        #     ),
        #     actions=[
        #         flet.TextButton("Retry", on_click=self.checkICStatus),
        #         flet.TextButton("Quit", on_click=lambda _ : self.page.window_close()),
        #     ],
        # )

        # def checkICStatus(self):
        #     self.page.banner = self.ICBanner
        #     self.page.update()
        #     if connect():
        #         self.page.banner.open = False
        #         self.page.update()
        #     else:
        #         self.page.banner.open = True
        #         self.page.update()

        # checkICStatus()
    
    def init(self):
        self.page.on_route_change = self.on_route_change
        # self.page.on_view_pop = self.view_pop
        # self.checkICStatus()
        global selectedIndex
        selectedIndex = 0
        token = self.load_token()
        if authentication.authenticate_token(token):
            self.page.go('/home')
        else:
            self.page.go('/authentication')
    
    def on_route_change(self, route: flet.RouteChangeEvent):
        new_page = {
            "/authentication": Authentication,
            "/home": Home,
            "/quiz": AbilityQuiz,
            "/practise": TargetedPractice

        }[self.page.route](self.page)

        self.page.views.clear()
        self.page.views.append(
            flet.View(route, [new_page])
        )
    
    # def view_pop(self, e: flet.ViewPopEvent):
    #     self.page.views.pop()
    #     top_view: flet.View = self.page.views[-1]
    #     self.page.go(top_view.route)
    #     self.page.update()

    def load_token(self):
        try:
            with open('token.pickle', 'rb') as f:
                token = pickle.load(f)
            return token
        except:
            return None

    

class Authentication(flet.Row):
    def __init__(self, page: flet.Page):
        super().__init__()
        print("AUTHENTICATION")
        self.expand = True
        self.imageColumn = flet.Column(
            controls = [
                flet.Image(
                    src='https://img.freepik.com/free-photo/painting-mountain-lake-with-mountain-background_188544-9126.jpg',
                    opacity=0.9,
                    fit=flet.ImageFit.COVER,
                    expand=True
                )
            ],
            expand=True
        )

        # Sign In

        self.signInErrorDialog = flet.AlertDialog(
            modal=True,
            title=flet.Text("Invalid credentials", style=flet.TextThemeStyle.LABEL_LARGE, size=20),
            content=flet.Text("Please try again or Sign up."),
            actions=[
                flet.ElevatedButton("Retry", on_click=lambda _ : page.close_dialog()),
                flet.ElevatedButton("Sign Up", on_click=self.signInToSignUp),
            ],
            actions_alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
            on_dismiss=self.signInError
        )

        self.emailSignIn=flet.TextField(
            label='Email address',
            icon=flet.icons.MAIL,
            color=TEXT,
            border_color=SECONDARY,
            cursor_color=SECONDARY,
            focused_border_color=SECONDARY,
            focused_color=SECONDARY,
            keyboard_type='email',
            autocorrect=False,
            dense=True,
            on_submit=self.validSignInEmail,
            on_change=self.validate_signIn
        )

        self.passSignIn=flet.TextField(
            label='Password',
            icon=flet.icons.LOCK,
            color=TEXT,
            border_color=SECONDARY,
            cursor_color=SECONDARY,
            focused_border_color=SECONDARY,
            focused_color=SECONDARY,
            keyboard_type='password',
            autocorrect=False,
            dense=True,
            password=True,
            can_reveal_password=True,
            on_change=self.validate_signIn,
            on_submit=self.validSignInPassword,
            error_text=""
        )

        self.signInButton=flet.ElevatedButton(
            text="Sign in",
            color=SECONDARY,
            bgcolor=PRIMARY,
            height=40,
            disabled = True,
            expand=True,
            on_click=self.signIn
        )

        self.clearSignInButton=flet.IconButton(
            icon=flet.icons.CLOSE_ROUNDED,
            style=flet.ButtonStyle(
                bgcolor=flet.colors.BLUE_200,
                shape={
                    flet.MaterialState.HOVERED: flet.RoundedRectangleBorder(radius=10),
                    flet.MaterialState.DEFAULT: flet.RoundedRectangleBorder(radius=50),
                },
            ),
            on_click=self.clearSignIn,
            tooltip="Clear section"
        )

        # Sign Up

        self.signUpErrorDialog = flet.AlertDialog(
            modal=True,
            title=flet.Text("Error encountered when creating account", style=flet.TextThemeStyle.LABEL_LARGE, size=20),
            content=flet.Text("Please try again or Sign in."),
            actions=[
                flet.ElevatedButton("Retry", on_click=lambda _ : page.close_dialog()),
                flet.ElevatedButton("Sign In", on_click=self.signUpToSignIn),
            ],
            actions_alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
            on_dismiss=self.signUpError
        )

        self.emailSignUp=flet.TextField(
            label='Email address',
            icon=flet.icons.MAIL,
            color=TEXT,
            border_color=SECONDARY,
            cursor_color=SECONDARY,
            focused_border_color=SECONDARY,
            focused_color=SECONDARY,
            keyboard_type='email',
            autocorrect=False,
            dense=True,
            on_submit=self.validSignUpEmail,
            on_change=self.validate_signUp
        )

        self.passSignUp=flet.TextField(
            label='Password',
            icon=flet.icons.LOCK,
            color=TEXT,
            border_color=SECONDARY,
            cursor_color=SECONDARY,
            focused_border_color=SECONDARY,
            focused_color=SECONDARY,
            keyboard_type='password',
            autocorrect=False,
            dense=True,
            password=True,
            can_reveal_password=True,
            on_change=self.validate_signUp,
            on_submit=self.validSignUpPassword,
        )

        self.mtSelection = flet.Dropdown(
            label="Mother-tongue language",
            options=[
                flet.dropdown.Option('Chinese'),
            ],
            dense=True,
            icon=flet.icons.LANGUAGE,
            color=TEXT,
            text_size=17,
            border_color=SECONDARY,
            focused_border_color=SECONDARY,
            focused_color=SECONDARY,
            on_change=self.validate_signUp,
            expand=True
        )

        self.levelSelection = flet.Dropdown(
            label="Level",
            options=[
                flet.dropdown.Option('1'),
                flet.dropdown.Option('2'),
                flet.dropdown.Option('3'),
                flet.dropdown.Option('4'),
                flet.dropdown.Option('5'),
                flet.dropdown.Option('6'),
            ],
            dense=True,
            color=TEXT,
            text_size=17,
            border_color=SECONDARY,
            focused_border_color=SECONDARY,
            focused_color=SECONDARY,
            expand=True,
            prefix=flet.Text('Primary '),
            on_change=self.validate_signUp,
        )

        self.tcCheckbox = flet.Checkbox(
            label="By signing up for an account, I agree to the Terms and Conditions",
            label_position='right',
            fill_color=TERTIARY,
            on_change=self.validate_signUp,
            expand=True,
        )

        self.signUpButton=flet.ElevatedButton(
            text="Sign up",
            color=SECONDARY,
            bgcolor=PRIMARY,
            height=40,
            disabled = True,
            expand=True,
            on_click=self.signUp
        )

        self.clearSignUpButton=flet.IconButton(
            icon=flet.icons.CLOSE_ROUNDED,
            style=flet.ButtonStyle(
                bgcolor=flet.colors.BLUE_200,
                shape={
                    flet.MaterialState.HOVERED: flet.RoundedRectangleBorder(radius=10),
                    flet.MaterialState.DEFAULT: flet.RoundedRectangleBorder(radius=50),
                },
            ),
            on_click=self.clearSignUp,
            tooltip="Clear section",
        )

        
        self.controls = [
            self.imageColumn,

            flet.VerticalDivider(
                color=TERTIARY,
                thickness = 3,
                width = 8,
            ),

            flet.Column(
                controls = [
                    flet.Container(
                        content=(authTabs:=flet.Tabs(
                            tabs = [
                                flet.Tab(
                                    text="Sign In",
                                    content=flet.Container(
                                        content=flet.Column(
                                            controls=[
                                                flet.Column(
                                                    controls=[
                                                        flet.Text(value='Welcome back!', size=34,color=SECONDARY, weight='w700'),
                                                        flet.Text(value='Log in to your account', size=20,color=TEXT, weight='w300')
                                                    ],
                                                    spacing=-50,
                                                ),
                                                
                                                flet.Container(
                                                    content=flet.Icon(name='lock_person',size=200, color=TERTIARY),
                                                    alignment=flet.alignment.center,
                                                ),

                                                flet.Column(
                                                    controls=[
                                                        self.emailSignIn,

                                                        self.passSignIn,

                                                        flet.Container(
                                                            content=flet.Row(
                                                                controls=[
                                                                    self.clearSignInButton,
                                                                    self.signInButton
                                                                ]
                                                            ),
                                                            alignment=flet.alignment.center,
                                                        ),
                                                    ],
                                                    expand=True,
                                                    spacing=20,
                                                    alignment=flet.CrossAxisAlignment.CENTER
                                                ),
                                                
                                            ],
                                            expand=True,
                                            spacing=30,
                                            alignment=flet.MainAxisAlignment.CENTER,
                                            horizontal_alignment=flet.MainAxisAlignment.END
                                        ),
                                        padding=20,
                                        expand=True
                                    ),
                                ),
                                flet.Tab(
                                    text="Sign Up",
                                    content=flet.Container(
                                        content=flet.Column(
                                            controls=[
                                                flet.Column(
                                                    controls=[
                                                        flet.Text(value='Welcome!', size=34,color=SECONDARY, weight='w700'),
                                                        flet.Text(value="Let's create your account", size=20,color=TEXT, weight='w300')
                                                    ],
                                                    spacing=-50,
                                                ),
                                                
                                                flet.Container(
                                                    content=flet.Icon(name='person',size=100,color=TERTIARY),
                                                    alignment=flet.alignment.center,
                                                ),

                                                flet.Column(
                                                    controls=[
                                                        self.emailSignUp,

                                                        self.passSignUp,

                                                        flet.Row(
                                                            controls=[
                                                                self.mtSelection,
                                                                self.levelSelection,
                                                            ],
                                                            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                                                            spacing=10
                                                        ),
                                                        
                                                    ],
                                                    expand=True,
                                                    spacing=15,
                                                    alignment=flet.CrossAxisAlignment.CENTER
                                                ),

                                                flet.Column(
                                                    controls=[
                                                        self.tcCheckbox,

                                                        flet.Container(
                                                            content=flet.Row(
                                                                controls=[
                                                                    self.clearSignUpButton,
                                                                    self.signUpButton
                                                                ]
                                                            ),
                                                            alignment=flet.alignment.center,
                                                        ),
                                                    ],
                                                    expand=True,
                                                    alignment=flet.MainAxisAlignment.CENTER
                                                ),
                                                
                                            ],
                                            expand=True,
                                            spacing=25,
                                            alignment=flet.MainAxisAlignment.CENTER,
                                            horizontal_alignment=flet.MainAxisAlignment.END
                                        ),
                                        padding=20,
                                        expand=True
                                    ),
                                ),
                            ],
                            animation_duration = 300,
                            width = (page.window_width/2) - 30,
                            height = page.window_height,
                            scrollable=True,
                            expand=True,
                        )),
                        expand=True,
                        alignment=flet.alignment.center
                    )
                    
                ],
                alignment=flet.MainAxisAlignment.CENTER,
                horizontal_alignment=flet.MainAxisAlignment.CENTER,
                expand=True
            ),
        ]

        self.width = page.window_width,
        self.height = page.window_height,
        self.vertical_alignment = flet.CrossAxisAlignment.START,
        self.spacing=0,
        self.alignment = flet.MainAxisAlignment.START,
        self.expand=True
    
    def signIn(self, e: flet.ControlEvent):
        token = authentication.login_user(self.emailSignIn.value, self.passSignIn.value)
        self.page.update()

        if token:
            authentication.store_session(token)
            print("WENT 1")
            self.page.go('/home')
            print("WENT 2")
            # self.page.update()
        else:
            self.page.dialog = self.signInErrorDialog
            self.page.dialog.open = True
            self.page.update()

    
    def clearSignIn(self, e: flet.ControlEvent):
        self.emailSignIn.value, self.passSignIn.value = None, None
        self.page.update()

    def signInToSignUp(self, e: flet.ControlEvent):
        self.page.close_dialog()
        self.authTabs.selected_index = 1
        self.page.update()

    def validSignInEmail(self, e: flet.ControlEvent):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, self.emailSignIn.value):
            self.emailSignIn.error_text = ""
            self.passSignIn.focus()
            self.page.update()
        else:
            self.emailSignIn.error_text = "Enter a valid email address"
            self.page.update()
    
    def is_validSignInEmail(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        self.page.update()
        return re.match(pattern, self.emailSignIn.value)

    def validSignInPassword(self, e: flet.ControlEvent):
        if len(self.passSignIn.value)>7:
            self.passSignIn.error_text = ""
            self.page.update()
            
        else:
            self.passSignIn.error_text = "Password must be at least 8 characters long"
            self.page.update()

    def is_validSignInPassword(self):
        self.page.update()
        return len(self.passSignIn.value)>7

    def validate_signIn(self, e: flet.ControlEvent):
        if all([self.emailSignIn.value, self.passSignIn.value, self.is_validSignInEmail(), self.is_validSignInPassword()]):
            self.signInButton.disabled = False
        else:
            self.signInButton.disabled=True
        
        self.page.update()

    def signInError(self, e: flet.ControlEvent):
        try:
            self.page.update() 
            account = database.child('users').order_by_child('email').equal_to(self.emailSignIn.value).get().val()
            self.passSignIn.value = None
            self.emailSignIn.error_text = "Incorrect password"
            self.page.update() 
        except:
            self.emailSignIn.error_text = "Account not found. Sign up instead?"
            self.emailSignIn.value, self.passSignIn.value = None, None
            self.page.update()

    def signUp(self, e: flet.ControlEvent):
        user = authentication.create_user(self.emailSignUp.value, self.passSignUp.value, self.mtSelection.value, self.levelSelection.value)
        if user:
            token = authentication.login_user(self.emailSignUp.value, self.passSignUp.value)
            authentication.store_session(token)
            self.page.update()
            self.page.go('/home')
        else:
            # self.page.dialog = self.signUpError
            self.page.show_dialog(self.signUpErrorDialog)
            self.page.update()

    def clearSignUp(self, e: flet.ControlEvent):
        self.emailSignUp.value, self.passSignUp.value, self.mtSelection.value, self.levelSelection.value, self.tcCheckbox.value = None, None, None, None, None
        self.page.update()

    def signUpToSignIn(self, e: flet.ControlEvent):
        self.page.close_dialog()
        self.authTabs.selected_index = 0
        self.page.update()

    def validSignUpEmail(self, e: flet.ControlEvent):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, self.emailSignUp.value):
            self.emailSignUp.error_text = ""
            self.passSignUp.focus()
            self.page.update()
        else:
            self.emailSignUp.error_text = "Enter a valid email address"
            self.page.update()
    
    def is_validSignUpEmail(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        self.page.update()
        return re.match(pattern, self.emailSignUp.value)

    def validSignUpPassword(self, e: flet.ControlEvent):
        if len(self.passSignUp.value)>7:
            self.passSignUp.error_text = ""
            self.page.update()
            
        else:
            self.passSignUp.error_text = "Password must be at least 8 characters long"
            self.page.update()

    def is_validSignUpPassword(self):
        self.page.update()
        return len(self.passSignUp.value)>7

    def validate_signUp(self, e: flet.ControlEvent):
        if all([self.emailSignUp.value, self.passSignUp.value, self.mtSelection.value, self.levelSelection.value, self.tcCheckbox.value, self.is_validSignUpEmail(), self.is_validSignUpPassword()]):
            self.signUpButton.disabled = False
            self.page.update()
        else:
            self.signUpButton.disabled=True
            self.page.update()
        
        self.page.update()

    def signUpError(self, e: flet.ControlEvent):
        try:
            account = database.child('users').order_by_child('email').equal_to(self.emailSignUp.value).get().val()
            print('GOT A')
            self.emailSignUp.value, self.passSignUp.value, self.mtSelection.value, self.levelSelection.value, self.tcCheckbox.value = None, None, None, None, None
            self.emailSignUp.error_text = "Account already exists. Sign in instead."
            self.page.update()
        except:
            self.emailSignUp.error_text = "Enter a valid email address"
            self.emailSignUp.value, self.passSignUp.value = None, None
            self.page.update()

class Home(flet.Row):
    def __init__(self, page: flet.Page):
        super().__init__()
        print('HOME')
        page.update()
        self.expand = True
        self.alignment = flet.MainAxisAlignment.CENTER
        self.user_id = authentication.authenticate_token(authentication.load_token())
        self.user = authentication.load_user()
        self.user_level = int(database.child(f"users/{self.user_id}/ability_quiz_tries").get().val())
        print(self.user_id)
        page.update()

        self.lg = flet.ElevatedButton(
            self.user,
            # on_click=self.logout,
            expand=True
        )

        self.navigation_rail = NavigationRail(page)

        self.controls = [
            self.navigation_rail,

            flet.VerticalDivider(width=1),

            self.lg,
        ]

class AbilityQuiz(flet.Row):
    def __init__(self, page: flet.Page):
        super().__init__()
        print('Quiz')
        self.expand = True
        self.navigation_rail = NavigationRail(page)
        self.user_id = authentication.authenticate_token(authentication.load_token())
        self.user = authentication.load_user()
        self.controls=[
            self.navigation_rail,
            flet.VerticalDivider(width=1),
            flet.Container(bgcolor="red", content=flet.Text("AQ"))
        ]

class TargetedPractice(flet.Row):
    def __init__(self, page: flet.Page):
        super().__init__()
        print('Targeted Practice')
        self.expand = True
        self.user_id = authentication.authenticate_token(authentication.load_token())
        self.user = authentication.load_user()
        self.navigation_rail = NavigationRail(page)
        new_user = user['ability_quiz_tries'] == 0
        if new_user:
            # self.screen = 
        self.controls=[
            self.navigation_rail,
            flet.VerticalDivider(width=1),
            flet.Container(bgcolor="red", content=flet.Text("TP"))
        ]

def NavigationRail(page):
    global selectedIndex
    navigation_rail = flet.NavigationRail(
        selected_index=selectedIndex,
        label_type=flet.NavigationRailLabelType.SELECTED,
        min_width=50,
        elevation=20,
        group_alignment=-0.8,
        indicator_shape=flet.ContinuousRectangleBorder(radius = 20),
        leading=flet.Image(
            src='https://img.freepik.com/free-photo/painting-mountain-lake-with-mountain-background_188544-9126.jpg',
            opacity=0.9,
            fit=flet.ImageFit.COVER,
            expand=True,
            width=50
        ),
        trailing=flet.Column(
            controls=[
            #     flet.IconButton(
            #         icon="run_circle",
            #         disabled=True
            #     ),
                flet.IconButton(
                    icon="logout",
                    on_click=lambda e: logout(e, page=page),
                )
            ],
            alignment="spaceBetween"
        ),
        destinations=[
            flet.NavigationRailDestination(
                icon=flet.icons.HOUSE_OUTLINED, 
                selected_icon=flet.icons.HOUSE, 
                label="Home",
            ),
            flet.NavigationRailDestination(
                icon=flet.icons.QUIZ_OUTLINED,
                selected_icon=flet.icons.QUIZ,
                label="Ability Quiz"
            ),
            flet.NavigationRailDestination(
                icon=flet.icons.SETTINGS_OUTLINED,
                selected_icon=flet.icons.SETTINGS,
                label = "Targeted Practise"
            )
        ],
        on_change=lambda e : navigation(e, page=page),
    )

    def navigation(e: flet.ControlEvent, page: flet.Page):

        global selectedIndex
        selectedIndex = e.control.selected_index

        if e.control.selected_index == 0:
            page.go('/home')

        if e.control.selected_index == 1:
            page.go('/quiz')
        
        if e.control.selected_index == 2:
            page.go('/practise')

        page.update()

    def logout(e: flet.ControlEvent, page: flet.Page):
        authentication.revoke_token(authentication.load_token())
        page.go('/authentication')
        Authentication.authTabs.selectedIndex = 0

    return navigation_rail 

class QuestionCard(flet.UserControl):
    def __init__(self, ):


def main(page: flet.Page):

    # Page Configuration

    print(page.views,"\n\n\n")
    page.title = "Unolingo"
    page.theme_mode = "light"
    page.window_width = 1440
    page.window_min_width = 1040
    page.window_height = 800
    page.window_min_height = 650
    page.window_resizable = True
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.MainAxisAlignment.CENTER
    page.update()

    # def declareUser(email_address: str):
    #     try:
    #         user_info = database.child('users').order_by_child('email').equal_to(email_address).get().val()
    #         global user
    #         user = dict([*user_info.values()][0])
    #         global uid
    #         uid = user['localId']
    #         global username
    #         username = user['displayName']
    #         global email
    #         email = email_address
    #         global motherTongue
    #         motherTongue = database.child(f'users/{uid}/motherTongue').get().val()
    #         global level
    #         level = database.child(f'users/{uid}/level').get().val()
    #     except:
    #         ...

    # declareUser('')

    # Methods

    def route_change(e: flet.RouteChangeEvent):
        page.views.clear()
        checkICStatus()
        page.update()
        page.views.append(authenticationView)

        if page.route == '/home':
            checkICStatus()
            page.update()
            page.session.get('user')
            page.views.append(homeView)
        
        if page.route == '/tutorial':
            checkICStatus()
            page.update()
            page.session.get('user')
            page.views.append(tutorialView)

        if page.route == '/quiz':
            checkICStatus()
            page.update()
            page.session.get('user')
            page.views.append(quizView)

        if page.route == '/test':
            checkICStatus()
            page.update()
            page.session.get('user')
            page.views.append(testView)

        if page.route == '/settings':
            checkICStatus()
            page.update()
            page.session.get('user')
            page.views.append(settingsView)

        page.update()
    
    def view_pop(e: flet.ViewPopEvent) -> None:
        page.views.pop()
        top_view: flet.View = page.views[-1]
        page.go(top_view.route)
        page.update()

    def checkICStatus():
        page.banner = ICBanner
        page.update()
        if connect():
            page.banner.open = False
            page.update()
        else:
            page.banner.open = True
            page.update()

    # Sign In
    
    def signIn(e: flet.ControlEvent):
        checkICStatus()
        try:
            
            user_info = auth.sign_in_with_email_and_password(emailSignIn.value, passSignIn.value)
            user_info = database.child('users').child(user_info['localId']).get().val()
            print(user_info)
            auth.current_user = user_info
            page.session.set('user', dict(user_info))
            user = page.session.get('user')
            print('\n\n\n',user)
            homeBar.title = user['email']
            homeView.update()
            print('Done')
            page.go('/home')
            emailSignIn.value, passSignIn.value = None, None
            emailSignIn.error_text, passSignIn.error_text = '', ''
            page.update()
        except:
            checkICStatus()
            page.show_dialog(signInErrorDialog)
            page.update()

    def clearSignIn(e: flet.ControlEvent):
        emailSignIn.value, passSignIn.value = None, None
        page.update()

    def signInToSignUp(e: flet.ControlEvent):
        page.close_dialog()
        authTabs.selected_index = 1
        page.update()

    def signInError(e: flet.ControlEvent):
        print('S ERROR')
        try:
            account = database.child('users').order_by_child('email').equal_to(emailSignIn.value).get().val()
            passSignIn.value = None
            emailSignIn.error_text = "Incorrect password"
            page.update() 
        except:
            emailSignIn.error_text = "Account not found. Sign up instead?"
            emailSignIn.value, passSignIn.value = None, None
            page.update()

    def validSignInEmail(e: flet.ControlEvent):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, emailSignIn.value):
            emailSignIn.error_text = ""
            passSignIn.focus()
            page.update()
        else:
            emailSignIn.error_text = "Enter a valid email address"
            page.update()
    
    def is_validSignInEmail():
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        page.update()
        return re.match(pattern, emailSignIn.value)

    def validSignInPassword(e: flet.ControlEvent):
        if len(passSignIn.value)>7:
            passSignIn.error_text = ""
            page.update()
            
        else:
            passSignIn.error_text = "Password must be at least 8 characters long"
            page.update()

    def is_validSignInPassword():
        page.update()
        return len(passSignIn.value)>7

    def validate_signIn(e: flet.ControlEvent):
        if all([emailSignIn.value, passSignIn.value, is_validSignInEmail(), is_validSignInPassword()]):
            signInButton.disabled = False
        else:
            signInButton.disabled=True
        
        page.update()

    # Sign Up
    
    def signUp(e: flet.ControlEvent):
        checkICStatus()
        page.update()
        try:
            global user
            user = auth.create_user_with_email_and_password(emailSignUp.value,passSignUp.value)
            user['displayName'] = user['email'][:(user['email'].find('@'))]
            user = database.child(f"users/{user['localId']}").set(user)
            auth.current_user = user
            page.session.set('user', user)
            tBar.title = flet.Text(dict(user)['email'])
            # page.update()
            print(page.session.get('user'))
            page.go('/tutorial')
            emailSignUp.value, passSignUp.value, mtSelection.value, levelSelection.value, tcCheckbox.value = None, None, None, None, None
            emailSignUp.error_text = ''
            passSignUp.error_text = '2'
            page.update()
        except:
            page.show_dialog(signUpErrorDialog)
            page.update()

    def clearSignUp(e: flet.ControlEvent):
        emailSignUp.value, passSignUp.value, mtSelection.value, levelSelection.value, tcCheckbox.value = None, None, None, None, None
        page.update()

    def signUpToSignIn(e: flet.ControlEvent):
        page.close_dialog()
        authTabs.selected_index = 0
        page.update()
    
    def signUpError(e: flet.ControlEvent):
        try:
            account = database.child('users').order_by_child('email').equal_to(emailSignUp.value).get().val()
            print('GOT A')
            emailSignUp.value, passSignUp.value, mtSelection.value, levelSelection.value, tcCheckbox.value = None, None, None, None, None
            emailSignUp.error_text = "Account already exists. Sign in instead."
            page.update()
        except:
            checkICStatus()
            emailSignUp.error_text = "Enter a valid email address"
            emailSignUp.value, passSignUp.value = None, None
            page.update()

    def validSignUpEmail(e: flet.ControlEvent):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, emailSignUp.value):
            emailSignUp.error_text = ""
            passSignUp.focus()
            page.update()
        else:
            emailSignUp.error_text = "Enter a valid email address"
            page.update()
    
    def is_validSignUpEmail():
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        page.update()
        return re.match(pattern, emailSignUp.value)

    def validSignUpPassword(e: flet.ControlEvent):
        if len(passSignUp.value)>7:
            passSignUp.error_text = ""
            page.update()
            
        else:
            passSignUp.error_text = "Password must be at least 8 characters long"
            page.update()

    def is_validSignUpPassword():
        page.update()
        return len(passSignUp.value)>7

    def validate_signUp(e: flet.ControlEvent):
        if all([emailSignUp.value, passSignUp.value, mtSelection.value, levelSelection.value, tcCheckbox.value, is_validSignUpEmail(), is_validSignUpPassword()]):
            signUpButton.disabled = False
            page.update()
        else:
            signUpButton.disabled=True
            page.update()
        
        page.update()

    def logout(e: flet.ControlEvent):
        auth.current_user = None
        page.session.clear()
        page.go('/authentication')
        authTabs.selected_index=0
        emailSignIn.focus()
        page.update()

    # UI Elements

    ICBanner = flet.Banner(
        bgcolor=flet.colors.AMBER_100,
        leading=flet.Icon(flet.icons.WARNING_AMBER_ROUNDED, color=flet.colors.AMBER, size=40),
        content=flet.Text(
            "Oops, it seems like you are not connected to the internet.",
        ),
        actions=[
            flet.TextButton("Retry", on_click=checkICStatus),
            flet.TextButton("Quit", on_click=lambda _ : page.window_close()),
        ],
    )

    checkICStatus()

    imageColumn = flet.Column(
        controls = [
            flet.Image(
                src='https://img.freepik.com/free-photo/painting-mountain-lake-with-mountain-background_188544-9126.jpg',
                opacity=0.9,
                fit=flet.ImageFit.COVER,
                expand=True
            )
        ],
        expand=True
    )

    # Sign In

    signInErrorDialog = flet.AlertDialog(
        modal=True,
        title=flet.Text("Invalid credentials", style=flet.TextThemeStyle.LABEL_LARGE, size=20),
        content=flet.Text("Please try again or Sign up."),
        actions=[
            flet.ElevatedButton("Retry", on_click=lambda _ : page.close_dialog()),
            flet.ElevatedButton("Sign Up", on_click=signInToSignUp),
        ],
        actions_alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
        on_dismiss=signInError,
    )

    emailSignIn=flet.TextField(
        label='Email address',
        icon=flet.icons.MAIL,
        color=TEXT,
        border_color=SECONDARY,
        cursor_color=SECONDARY,
        focused_border_color=SECONDARY,
        focused_color=SECONDARY,
        keyboard_type='email',
        autocorrect=False,
        dense=True,
        on_submit=validSignInEmail,
        on_change=validate_signIn
    )

    passSignIn=flet.TextField(
        label='Password',
        icon=flet.icons.LOCK,
        color=TEXT,
        border_color=SECONDARY,
        cursor_color=SECONDARY,
        focused_border_color=SECONDARY,
        focused_color=SECONDARY,
        keyboard_type='password',
        autocorrect=False,
        dense=True,
        password=True,
        can_reveal_password=True,
        on_change=validate_signIn,
        on_submit=validSignInPassword,
        error_text=""
    )

    signInButton=flet.ElevatedButton(
        text="Sign in",
        color=SECONDARY,
        bgcolor=PRIMARY,
        height=40,
        disabled = True,
        expand=True,
        on_click=signIn,
    )

    clearSignInButton=flet.IconButton(
        icon=flet.icons.CLOSE_ROUNDED,
        style=flet.ButtonStyle(
            bgcolor=flet.colors.BLUE_200,
            shape={
                flet.MaterialState.HOVERED: flet.RoundedRectangleBorder(radius=10),
                flet.MaterialState.DEFAULT: flet.RoundedRectangleBorder(radius=50),
            },
        ),
        on_click=clearSignIn,
        tooltip="Clear section"
    )

    # Sign Up

    signUpErrorDialog = flet.AlertDialog(
        modal=True,
        title=flet.Text("Error encountered when creating account", style=flet.TextThemeStyle.LABEL_LARGE, size=20),
        content=flet.Text("Please try again or Sign in."),
        actions=[
            flet.ElevatedButton("Retry", on_click=lambda _ : page.close_dialog()),
            flet.ElevatedButton("Sign In", on_click=signUpToSignIn),
        ],
        actions_alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
        on_dismiss=signUpError,
            
    )

    emailSignUp=flet.TextField(
        label='Email address',
        icon=flet.icons.MAIL,
        color=TEXT,
        border_color=SECONDARY,
        cursor_color=SECONDARY,
        focused_border_color=SECONDARY,
        focused_color=SECONDARY,
        keyboard_type='email',
        autocorrect=False,
        dense=True,
        on_submit=validSignUpEmail,
        on_change=validate_signUp
    )

    passSignUp=flet.TextField(
        label='Password',
        icon=flet.icons.LOCK,
        color=TEXT,
        border_color=SECONDARY,
        cursor_color=SECONDARY,
        focused_border_color=SECONDARY,
        focused_color=SECONDARY,
        keyboard_type='password',
        autocorrect=False,
        dense=True,
        password=True,
        can_reveal_password=True,
        on_change=validate_signUp,
        on_submit=validSignUpPassword,
        error_text=""
    )

    mtSelection = flet.Dropdown(
        label="Mother-tongue language",
        options=[
            flet.dropdown.Option('Chinese'),
        ],
        dense=True,
        icon=flet.icons.LANGUAGE,
        color=TEXT,
        text_size=17,
        border_color=SECONDARY,
        focused_border_color=SECONDARY,
        focused_color=SECONDARY,
        on_change=validate_signUp,
        expand=True
    )

    levelSelection = flet.Dropdown(
        label="Level",
        options=[
            flet.dropdown.Option('1'),
            flet.dropdown.Option('2'),
            flet.dropdown.Option('3'),
            flet.dropdown.Option('4'),
            flet.dropdown.Option('5'),
            flet.dropdown.Option('6'),
        ],
        dense=True,
        color=TEXT,
        text_size=17,
        border_color=SECONDARY,
        focused_border_color=SECONDARY,
        focused_color=SECONDARY,
        expand=True,
        prefix=flet.Text('Primary '),
        on_change=validate_signUp,
    )

    tcCheckbox = flet.Checkbox(
        label="By signing up for an account, I agree to the Terms and Conditions",
        label_position='right',
        fill_color=TERTIARY,
        on_change=validate_signUp,
        expand=True
    )

    signUpButton=flet.ElevatedButton(
        text="Sign up",
        color=SECONDARY,
        bgcolor=PRIMARY,
        height=40,
        disabled = True,
        expand=True,
        on_click=signUp,
    )

    clearSignUpButton=flet.IconButton(
        icon=flet.icons.CLOSE_ROUNDED,
        style=flet.ButtonStyle(
            bgcolor=flet.colors.BLUE_200,
            shape={
                flet.MaterialState.HOVERED: flet.RoundedRectangleBorder(radius=10),
                flet.MaterialState.DEFAULT: flet.RoundedRectangleBorder(radius=50),
            },
        ),
        on_click=clearSignUp,
        tooltip="Clear section",
    )

    checkICStatus()
    page.update()
    user = page.session.get('user')

    # Authentication View

    authenticationView = flet.View(
        route = '/authentication',
        controls = [
            flet.Row(
                controls = [
                    imageColumn,

                    flet.VerticalDivider(
                        color=TERTIARY,
                        thickness = 3,
                        width = 8,
                    ),

                    flet.Column(
                        controls = [
                            flet.Container(
                                content=(authTabs:=flet.Tabs(
                                    tabs = [
                                        flet.Tab(
                                            text="Sign In",
                                            content=flet.Container(
                                                content=flet.Column(
                                                    controls=[
                                                        flet.Column(
                                                            controls=[
                                                                flet.Text(value='Welcome back!', size=34,color=SECONDARY, weight='w700'),
                                                                flet.Text(value='Log in to your account', size=20,color=TEXT, weight='w300')
                                                            ],
                                                            spacing=-50,
                                                        ),
                                                        
                                                        flet.Container(
                                                            content=flet.Icon(name='lock_person',size=200, color=TERTIARY),
                                                            alignment=flet.alignment.center,
                                                        ),

                                                        flet.Column(
                                                            controls=[
                                                                emailSignIn,

                                                                passSignIn,

                                                                flet.Container(
                                                                    content=flet.Row(
                                                                        controls=[
                                                                            clearSignInButton,
                                                                            signInButton
                                                                        ]
                                                                    ),
                                                                    alignment=flet.alignment.center,
                                                                ),
                                                            ],
                                                            expand=True,
                                                            spacing=20,
                                                            alignment=flet.CrossAxisAlignment.CENTER
                                                        ),
                                                        
                                                    ],
                                                    expand=True,
                                                    spacing=30,
                                                    alignment=flet.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=flet.MainAxisAlignment.END
                                                ),
                                                padding=20,
                                                expand=True
                                            ),
                                        ),
                                        flet.Tab(
                                            text="Sign Up",
                                            content=flet.Container(
                                                content=flet.Column(
                                                    controls=[
                                                        flet.Column(
                                                            controls=[
                                                                flet.Text(value='Welcome!', size=34,color=SECONDARY, weight='w700'),
                                                                flet.Text(value="Let's create your account", size=20,color=TEXT, weight='w300')
                                                            ],
                                                            spacing=-50,
                                                        ),
                                                        
                                                        flet.Container(
                                                            content=flet.Icon(name='person',size=100,color=TERTIARY),
                                                            alignment=flet.alignment.center,
                                                        ),

                                                        flet.Column(
                                                            controls=[
                                                                emailSignUp,

                                                                passSignUp,

                                                                flet.Row(
                                                                    controls=[
                                                                        mtSelection,
                                                                        levelSelection,
                                                                    ],
                                                                    alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                                                                    spacing=10
                                                                ),
                                                                
                                                            ],
                                                            expand=True,
                                                            spacing=15,
                                                            alignment=flet.CrossAxisAlignment.CENTER
                                                        ),

                                                        flet.Column(
                                                            controls=[
                                                                tcCheckbox,

                                                                flet.Container(
                                                                    content=flet.Row(
                                                                        controls=[
                                                                            clearSignUpButton,
                                                                            signUpButton
                                                                        ]
                                                                    ),
                                                                    alignment=flet.alignment.center,
                                                                ),
                                                            ],
                                                            expand=True,
                                                            alignment=flet.MainAxisAlignment.CENTER
                                                        ),
                                                        
                                                    ],
                                                    expand=True,
                                                    spacing=25,
                                                    alignment=flet.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=flet.MainAxisAlignment.END
                                                ),
                                                padding=20,
                                                expand=True
                                            ),
                                        ),
                                    ],
                                    animation_duration = 300,
                                    width = (page.window_width/2) - 30,
                                    height = page.window_height,
                                    scrollable=True,
                                    expand=True,
                                )),
                                expand=True,
                                alignment=flet.alignment.center
                            )
                            
                        ],
                        alignment=flet.MainAxisAlignment.CENTER,
                        horizontal_alignment=flet.MainAxisAlignment.CENTER,
                        expand=True
                    ),
                ],
                width = page.window_width,
                height = page.window_height,
                vertical_alignment = flet.CrossAxisAlignment.START,
                spacing=0,
                alignment = flet.MainAxisAlignment.START,
                expand=True
            )
        ],
        bgcolor = BG,
        padding = 0
    )

    # Tutorial View
    
    tutorialView = flet.View(
        route='/tutorial',
        controls=[
            tBar:=flet.AppBar(
                leading=flet.Icon(flet.icons.HELP),
                leading_width=40,
                title=flet.Text(),
                center_title=False,
                bgcolor=flet.colors.SURFACE_VARIANT,
                actions=[
                    flet.IconButton(flet.icons.WB_SUNNY_OUTLINED),
                    flet.IconButton(flet.icons.FILTER_3,on_click=logout),
                    flet.PopupMenuButton(
                        items=[
                            flet.PopupMenuItem(text="Item 1"),
                            flet.PopupMenuItem(),  # divider
                            flet.PopupMenuItem(
                                text="Checked item", checked=False, on_click=lambda _ : print('clicked')
                            ),
                        ]
                    ),
                ],
            )
        ]
    )

    # Home View
    
    homeView = flet.View(
        route='/home',
        controls=[
            homeBar:=flet.AppBar(
                leading=flet.Icon(flet.icons.HOUSE),
                leading_width=40,
                title=flet.Text(),
                center_title=False,
                bgcolor=flet.colors.SURFACE_VARIANT,
                actions=[
                    flet.IconButton(flet.icons.WB_SUNNY_OUTLINED),
                    flet.IconButton(
                        flet.icons.FILTER_3,
                        on_click=logout
                    ),
                    flet.PopupMenuButton(
                        items=[
                            flet.PopupMenuItem(text="Item 1"),
                            flet.PopupMenuItem(),  # divider
                            flet.PopupMenuItem(
                                text="Checked item", checked=False, on_click=lambda _ : print('clicked')
                            ),
                        ]
                    ),
                ],
            )
        ]
    )

    # Quiz View
    
    quizView = flet.View(
        route='/quiz'
    )

    # Test View
    
    testView = flet.View(
        route='/test'
    )

    # Settings View
    
    settingsView = flet.View(
        route='/settings'
    )

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    checkICStatus()
    page.go(page.route)


if __name__  ==  "__main__":
    flet.app(target = Main, view = flet.FLET_APP)