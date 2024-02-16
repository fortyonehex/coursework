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

from questions import *

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

# Colour codes

PRIMARY = '#8AB1D0'
SECONDARY = '#0D1931'
TERTIARY = '#8D887C'
ACCENT = '#DD4055'
BG = '#F2EFE9'
TEXT = '#2E2F2F'

# pre-initialisation of quiz data
ability_quiz = parse_qn_data("ability_quiz.json")

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
            ],
            dense=True,
            color=TEXT,
            text_size=17,
            border_color=SECONDARY,
            focused_border_color=SECONDARY,
            focused_color=SECONDARY,
            expand=True,
            prefix=flet.Text('Secondary '),
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
        self.bgcolor = BG
        self.expand = True
        self.alignment = flet.MainAxisAlignment.START
        self.user_id = authentication.authenticate_token(authentication.load_token())
        self.user = authentication.load_user()
        self.current_user_name = authentication.get_name(authentication.load_token())
        self.user_level = int(database.child(f"users/{self.user_id}/ability_quiz_tries").get().val())

        print(self.user_id)
        page.update()

        self.navigation_rail = NavigationRail(page)

        self.controls = [
            self.navigation_rail,

            flet.VerticalDivider(width=1),

            flet.Column(
                controls = [
                    flet.Text(
                        value="\n",
                        size=1,
                        color='#5a5c69',
                        weight=flet.FontWeight.W_300
                    ),

                    flet.Row(
                        controls=[

                            flet.Text(
                                value="Hello,",
                                size=30,
                                color='#5a5c69',
                                weight=flet.FontWeight.W_300

                            ),
                            flet.Text(
                                value=self.user['display_name'],
                                size=30,
                                color='#5a5c69',
                                weight=flet.FontWeight.W_700,
                            )
                        ],
                        alignment=flet.MainAxisAlignment.START,
                    ),

                    flet.Text("Personal Achievements", style=flet.TextThemeStyle.TITLE_LARGE, weight="bold"),
                    
                    flet.Row(
                        controls=[
                            flet.Container(
                                padding=30,
                                alignment=flet.alignment.center,
                                bgcolor='white',
                                shadow=flet.BoxShadow(
                                    # spread_radius=1,
                                    blur_radius=10,
                                    color=TEXT
                                ),
                                border=flet.border.only(
                                    left=flet.border.BorderSide(5, color='yellow')),
                                content=flet.Row(
                                    alignment='spaceBetween',
                                    vertical_alignment='center',
                                    controls=[
                                        flet.Column(
                                            spacing=0,
                                            alignment='center',
                                            # horizontal_alignment='center',
                                            controls=[
                                                flet.Text(
                                                    value="Attempts of Ability Quiz",
                                                    color=PRIMARY,
                                                ),
                                               flet. Text(
                                                    value=self.user['ability_quiz_tries'],
                                                    color=SECONDARY,
                                                    size=25,
                                                    weight=flet.FontWeight.W_600
                                                )
                                            ]
                                        ),
                                        flet.Icon(
                                            "quiz_outlined",
                                            color='#dddfeb',
                                            size=50
                                        )
                                    ]
                                ),
                                border_radius=20
            

                            ),

                            flet.Container(
                                padding=30,
                                alignment=flet.alignment.center,
                                bgcolor='white',
                                shadow=flet.BoxShadow(
                                    # spread_radius=1,
                                    blur_radius=10,
                                    color=TEXT
                                ),
                                border=flet.border.only(
                                    left=flet.border.BorderSide(5, color='green')),
                                content=flet.Row(
                                    alignment='spaceBetween',
                                    vertical_alignment='center',
                                    controls=[
                                        flet.Column(
                                            spacing=0,
                                            alignment='center',
                                            # horizontal_alignment='center',
                                            controls=[
                                                flet.Text(
                                                    value="Highest Score for Ability Quiz",
                                                    color=PRIMARY,
                                                ),
                                               flet. Text(
                                                    value=self.user["ability_quiz_score"],
                                                    color=SECONDARY,
                                                    size=25,
                                                    weight=flet.FontWeight.W_600
                                                )
                                            ]
                                        ),
                                        flet.Icon(
                                            "numbers_outlined",
                                            color='#dddfeb',
                                            size=50
                                        )
                                    ]
                                ),
                                border_radius=20

                            ),

                            flet.Container(
                                padding=30,
                                alignment=flet.alignment.center,
                                bgcolor='white',
                                shadow=flet.BoxShadow(
                                    # spread_radius=1,
                                    blur_radius=10,
                                    color=TEXT
                                ),
                                border=flet.border.only(
                                    left=flet.border.BorderSide(5, color='blue')),
                                content=flet.Row(
                                    alignment='spaceBetween',
                                    vertical_alignment='center',
                                    controls=[
                                        flet.Column(
                                            spacing=0,
                                            alignment='center',
                                            # horizontal_alignment='center',
                                            controls=[
                                                flet.Text(
                                                    value="Attempts of Targeted Practice",
                                                    color=PRIMARY,
                                                ),
                                               flet. Text(
                                                    value=self.user["targeted_practice_tries"],
                                                    color=SECONDARY,
                                                    size=25,
                                                    weight=flet.FontWeight.W_600
                                                )
                                            ]
                                        ),
                                        flet.Icon(
                                            "run_circle_outlined",
                                            color='#dddfeb',
                                            size=50
                                        )
                                    ]
                                ),
                                border_radius=20
                            ),

                            flet.Container(
                                padding=30,
                                alignment=flet.alignment.center,
                                bgcolor='white',
                                shadow=flet.BoxShadow(
                                    # spread_radius=1,
                                    blur_radius=10,
                                    color=TEXT
                                ),
                                border=flet.border.only(
                                    left=flet.border.BorderSide(5, color='red')),
                                content=flet.Row(
                                    alignment='spaceBetween',
                                    vertical_alignment='center',
                                    controls=[
                                        flet.Column(
                                            spacing=0,
                                            alignment='center',
                                            # horizontal_alignment='center',
                                            controls=[
                                                flet.Text(
                                                    value="Competency of Targeted Practice",
                                                    color=PRIMARY,
                                                ),
                                               flet. Text(
                                                    value=self.user["targeted_practice_level"],
                                                    color=SECONDARY,
                                                    size=25,
                                                    weight=flet.FontWeight.W_600
                                                )
                                            ]
                                        ),
                                        flet.Icon(
                                            "numbers",
                                            color='#dddfeb',
                                            size=50
                                        )
                                    ]
                                ),
                                border_radius=20
                            ),
                        ],
                        wrap=True,
                        expand=True
                    )
                    
                ],
                spacing = 30,
                expand=True
            )
        ]

        self.spacing = 20

        self.alignment = "start"

class AbilityQuiz(flet.Row):
    def __init__(self, page: flet.Page):
        super().__init__()
        print('AbilityQuiz')
        page.update()
        self.bgcolor = 'red'
        self.expand = True
        self.alignment = flet.MainAxisAlignment.START
        self.user_id = authentication.authenticate_token(authentication.load_token())
        self.user = authentication.load_user()
        self.user_level = int(database.child(f"users/{self.user_id}/ability_quiz_tries").get().val())
        page.session.set("ability_curr_page", 0)

        ability_quiz_questions = ability_quiz[0]["sections"] + ability_quiz[1]["sections"]
        
        self.navigation_rail = NavigationRail(page)
        self.controls = [
            self.navigation_rail,

            flet.VerticalDivider(width=1),

            AbilityQuizCard(ability_quiz_questions).build(page)
        ]

class TargetedPractice(flet.Row):
    def __init__(self, page: flet.Page):
        super().__init__()
        print('TargetedPractice')
        page.update()
        self.expand = True
        self.alignment = flet.MainAxisAlignment.START
        self.user_id = authentication.authenticate_token(authentication.load_token())
        self.user = authentication.load_user()
        self.user_level = int(database.child(f"users/{self.user_id}/ability_quiz_tries").get().val())
        new_user = self.user['ability_quiz_score'] == 0

        self.navigation_rail = NavigationRail(page)

        
        # DOESNT WORK - CANT CHECK IF NEW USER
        # if new_user:
        #     self.screen = flet.Column(
        #         flet.Text('AQ first'),
        #         flet.ElevatedButton(
        #             "AQ",
        #             on_click=self.toAbilityQuiz
        #         )
        #     )
        # else:
        self.screen = flet.Text("TargetedPractice")
        
        page.update()

        self.controls = [
            self.navigation_rail,

            flet.VerticalDivider(width=1),

            self.screen
        ]

    def toAbilityQuiz(e: flet.ControlEvent):
        global selectedIndex
        selectedIndex = 1

def NavigationRail(page):
    def logout(e: flet.ControlEvent):
        authentication.revoke_token(authentication.load_token())
        page.go('/authentication')
        Authentication.authTabs.selectedIndex = 0

    global selectedIndex
    navigation_rail = flet.NavigationRail(
        selected_index=selectedIndex,
        label_type=flet.NavigationRailLabelType.ALL,
        min_width=60,
        elevation=5,
        indicator_shape=flet.ContinuousRectangleBorder(radius = 20),
        leading=flet.Image(
            src='https://img.freepik.com/free-photo/painting-mountain-lake-with-mountain-background_188544-9126.jpg',
            opacity=0.9,
            fit=flet.ImageFit.COVER,
            expand=False,
            width=50
        ),
        trailing=flet.IconButton(
            icon="logout",
            on_click=logout
        ),
        group_alignment=-0.9,
        destinations=[
            flet.NavigationRailDestination(
                icon=flet.icons.HOUSE_OUTLINED, 
                selected_icon=flet.icons.HOUSE, 
                label="Home"
            ),
            flet.NavigationRailDestination(
                icon=flet.icons.QUIZ_OUTLINED,
                selected_icon=flet.icons.QUIZ,
                label="Ability Quiz",
            ),
            flet.NavigationRailDestination(
                icon=flet.icons.SETTINGS_OUTLINED,
                selected_icon=flet.icons.SETTINGS,
                label="Targeted Practise"
            ),
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

    return navigation_rail 

class AbilityQuizCard(flet.UserControl):
    def __init__(self, quiz):
        self.state = 0
        self.quiz = quiz

        self.scores = [None]*len(self.quiz)
        self.controls = []

    def refresh_questions(self):
        self.questions = list(self.quiz[self.state])
        self.instructions = self.quiz[self.state].instructions
        if type(self.quiz[self.state]) == PassageGroup:
            self.passage = self.quiz[self.state].text
        else:
            self.passage = ""
        self.selections = [None]*len(self.quiz[self.state])

    def build(self, page):
        self.page = page
        self.refresh_questions()
        self.rebuild()
        
        return flet.Row(controls=self.controls, width=page.width)

    def rebuild(self):
        tabs = []
        for i in range(len(self.questions)):
            options = [flet.Text("Q%d) " %(i+1) + self.questions[i].name, weight=flet.FontWeight.BOLD)]
            answers = []
            for j in range(len(self.questions[i].options)):
                options.append(flet.Text("    (%d) %s" %(j+1, self.questions[i].options[j])))
                answers.append(flet.Segment(value="%d,%d" %(i,j), label=flet.Text(str(j+1))))
            options.append(flet.SegmentedButton(
                segments=answers,
                allow_multiple_selection=False,
                allow_empty_selection=True,
                on_change=self.validate
            ))
            options.append(flet.Divider(height=1))
            #print(options)
            tabs += options

        self.button = flet.ElevatedButton(text="Next", disabled=True, on_click=self.nextpage)
        self.controls.append(flet.Container(
                                    content=flet.Column(controls=[
                                            flet.Text(self.instructions, weight=flet.FontWeight.BOLD),
                                            flet.Divider(height=1)] + 
                                            [flet.Text(i) for i in self.passage.split("\n")],
                                        expand=True,
                                        width=self.page.width*0.3,
                                        scroll=flet.ScrollMode.ALWAYS
                                    ), 
                                   # padding=10,
                                    alignment=flet.alignment.top_left
                                ))
        self.controls.append(flet.VerticalDivider(width=1))
        self.controls.append(flet.Column(
                                    controls=tabs+[self.button],
                                    scroll=flet.ScrollMode.ALWAYS,
                                    expand=True
                                ))

    def nextpage(self, e: flet.ControlEvent):
        self.grade_curr()

        self.state += 1
        del self.controls[0:3]
        self.refresh_questions()
        self.rebuild()

        if self.state == len(self.quiz)-1:
            self.button.text = "Submit"
            self.button.on_click = self.submit
        
        print(self.controls)
        self.page.update()

    def grade_curr(self):
        curr_score = self.quiz[self.state].grade(self.selections)
        self.scores[self.state] = curr_score

    def validate(self, e: flet.ControlEvent):
        print(e.control.selected)
        si, sj = list(e.control.selected)[0].split(",")
        # print(si, sj)
        self.selections[int(si)] = int(sj)
        if None not in self.selections:
            self.button.disabled = False
        else:
            self.button.disabled = True
        self.page.update()

    def submit(self, e: flet.ControlEvent):
        self.grade_curr()
        print(self.scores)
        exp_score_perc = (self.scores[0]+self.scores[1])/(len(self.quiz[0])+len(self.quiz[1]))
        hcl_score_perc = (self.scores[2]+self.scores[3])/(len(self.quiz[2])+len(self.quiz[3]))
        exp_grade = "proficient" if exp_score_perc > 0.67 else "mediocre" if exp_score_perc > 0.33 else "lacking"
        hcl_grade = "proficient" if hcl_score_perc > 0.67 else "mediocre" if hcl_score_perc > 0.33 else "lacking"

        del self.controls[0:3]
        self.controls.append(flet.Container(content=flet.Column(controls=[
            flet.Text("You are...", size=20),
            flet.Text(exp_grade, size=36, weight=flet.FontWeight.BOLD, spans=[flet.TextSpan(
                "  in Express Chinese, and", flet.TextStyle(size=20, weight=flet.FontWeight.NORMAL))]),
            flet.Text(hcl_grade, size=36, weight=flet.FontWeight.BOLD, spans=[flet.TextSpan(
                "  in Higher Chinese", flet.TextStyle(size=20, weight=flet.FontWeight.NORMAL))])
        ], alignment=flet.alignment.center), margin=100))
        self.page.update()

        # do some cloud shit here idk kavin pls fix

if __name__  ==  "__main__":
    flet.app(target = Main, view = flet.FLET_APP)