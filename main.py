# Imports
import os
import sys
import flet
import time
import base64
import random
import pyrebase
import urllib.request
from dotenv import load_dotenv

# Firebase configuration

## Retrieving configuration keys
# load_dotenv('.env')

# firebaseConfig = eval(os.getenv('CONFIG'))

# firebase = pyrebase.initialize_app(firebaseConfig)

# print('Initialised')

# database = firebase.database()

# storage = firebase.storage()

# auth = firebase.auth()

# while 1:
#     e = input('e: ')
#     p = input('p: ')
#     s = input('s: ')

#     if (e or p or s)  =  =  'q':
#         break

#     if s  =  =  'si':
#         try:
#             user = auth.sign_in_with_email_and_password(e,p)
#             print('S')
#             print(user)
#             user = database.child('users').child(user['localId'])
#             print('Here')
#             print(user['expiresIn'])
#             time.sleep(5)
#             print(user['expiresIn'])
#             print('Here')
#             print('\n\n' + storage.bucket.get_blob(user.child('displayName')).download_as_string())
#         except:
#             print('I')
#     elif s  =  =  'su':
#         try:
#             user = auth.create_user_with_email_and_password(e,p)
#             print('S')
#             user['displayName'] = user['email'][:(user['email'].find('@'))]
#             print('D')
#             database.child(f"users/{user['localId']}").set(user)
#             print('E')
#             storage.child('images/E').upload('EnviroMate Icon copy.png')
#             print('F')
#             print(storage.child('E').get_url(None))
#         except:
#             print('I')
#     else:
#         print('\nTRY AGAIN\n')

# print('Exited')

# Colour codes
PRIMARY = '#8AB1D0'
SECONDARY = '#0D1931'
TERTIARY = '#8D887C'
ACCENT = '#DD4055'
BG = '#F2EFE9'
TEXT = '#2E2F2F'

# Main app class

def main(page: flet.Page):

    # Page Configuration

    print(page.views)
    page.title = "test app 2"
    page.window_width = 1440
    page.window_min_width = 1040
    page.update()
    page.window_height = 900
    page.window_min_height = 650
    page.update()
    page.window_resizable = True
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.MainAxisAlignment.CENTER
    page.update()

    # Methods

    def ICBanner_status():
        if connect():
            ICBanner.open = True
        else:
            ICBanner.open = False
        
        page.update()

    def validate_signIn(e: flet.ControlEvent):
        if all([emailSignIn.value, passSignIn.value]):
            signInButton.disabled = False
        else:
            signInButton.disabled=True
        
        page.update()
    
    def signIn(e: flet.ControlEvent):
        print()

    def hover(e: flet.HoverEvent):
        clearSignIn.text = "Clear all"
        page.update()


    def route_change(e: flet.RouteChangeEvent):
        page.views.clear()
        page.views.append(ICView)
        # page.views.append(authenticationView)
        page.update()

    def resize(e: flet.ControlEvent):
        page.update()
        page.window_height = page.window_height
        page.window_width = page.window_width
        # tC.update()
        page.update()

    # Check internet access

    def connect(host='http://google.com'):
        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False

    # UI Elements

    ICBanner = flet.Banner(
        bgcolor=flet.colors.AMBER_100,
        leading=flet.Icon(flet.icons.WARNING_AMBER_ROUNDED, color=flet.colors.AMBER, size=40),
        content=flet.Text(
            "Oops, it seems like you are not connected to the internet."
        ),
        actions=[
            flet.TextButton("Retry", on_click=ICBanner_status),
            flet.TextButton("Quit", on_click=lambda _ : page.window_close()),
        ],
    )

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
        dense=False,
        on_submit=lambda _ : passSignIn.focus() if emailSignIn.value else None,
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
        dense=False,
        password=True,
        can_reveal_password=True,
        on_change=validate_signIn
    )

    signInButton=flet.ElevatedButton(
        text="Sign in",
        color=SECONDARY,
        bgcolor=PRIMARY,
        width=100,
        height=emailSignIn.height,
        disabled = True,
        # expand=True,
    )

    clearSignIn=flet.IconButton(
        icon=flet.icons.CLOSE_ROUNDED,
        style=flet.ButtonStyle(
            bgcolor=flet.colors.BLUE_200,
            elevation={"pressed": 0, "": 1},
            shape={
                flet.MaterialState.HOVERED: flet.RoundedRectangleBorder(radius=10),
                flet.MaterialState.DEFAULT: flet.RoundedRectangleBorder(radius=50),
            },
        )
    )
    
    # No Internet Connection View

    ICView = flet.View(
        route='/503',
        controls=[
            flet.Container(
                bgcolor='red',
                alignment=flet.alignment.center,
                expand=True
            )
        ]
    )

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
                                content=flet.Tabs(
                                    tabs = [
                                        flet.Tab(
                                            text="Sign In",
                                            content=flet.Container(
                                                content=flet.Column(
                                                    controls=[
                                                        flet.Text(value='Welcome back!', size=24,color=SECONDARY, weight='bold'),

                                                        flet.Container(
                                                            content=flet.Icon(name='mail'),
                                                            alignment=flet.alignment.center
                                                        ),

                                                        flet.Column(
                                                            controls=[
                                                                emailSignIn,

                                                                passSignIn,

                                                                flet.Container(
                                                                    content=flet.Row(
                                                                        controls=[
                                                                            clearSignIn,
                                                                            signInButton
                                                                        ]
                                                                    ),
                                                                    alignment=flet.alignment.center,
                                                                ),
                                                            ],
                                                            expand=True,
                                                            spacing=15,
                                                            alignment=flet.CrossAxisAlignment.STRETCH
                                                        ),
                                                        
                                                    ],
                                                    expand=True,
                                                    spacing=100,
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
                                                content=flet.Text("This is Tab 2")
                                            ),
                                        ),
                                    ],
                                    animation_duration = 300,
                                    width = (page.window_width/2) - 30,
                                    height = page.window_height,
                                    scrollable=True,
                                    expand=True,
                                ),
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

    

    # def colors(e: flet.ControlEvent):
    #     page.update()
    #     q.bgcolor = PRIMARY if e.control.selected_index  =  =  0 else ACCENT
    #     page.update()

    # x = flet.NavigationBar(
    #     destinations = [
    #         flet.NavigationDestination(icon = flet.icons.EXPLORE, label = "Explore", tooltip = "Time to explore"),
    #         flet.NavigationDestination(icon = flet.icons.COMMUTE, label = "Commute", tooltip = "Let's commute"),
    #         flet.NavigationDestination(
    #             icon = flet.icons.BOOKMARK_BORDER,
    #             selected_icon = flet.icons.BOOKMARK,
    #             label = "Book",
    #             tooltip = "Books are good",
    #         ),
    #     ],
    #     on_change = colors
    # )

    # page.add(
    #     (z: = flet.Column(
    #         expand = True,
    #         controls = [
    #             (y : =  flet.Container(
    #                 expand = 1,
    #                 content = (q: = flet.Text("Container 1"))
    #             )),
    #             flet.Container(
    #                 expand = 2, content = flet.Text("Container 2")
    #             ),
    #         ],
    #     ))
        
    # )

    page.on_resize = resize
    page.on_route_change = route_change
    page.go('/503')
    



if __name__  ==  "__main__":
    flet.app(target = main, view = flet.FLET_APP)