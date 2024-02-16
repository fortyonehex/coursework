# # Imports
# import os
# import re
# import sys
# from turtle import home
# import flet
# import time
# import base64
# import random
# import asyncio
# import pyrebase
# import urllib.request
# from dotenv import load_dotenv

# # Retrieving configuration keys

# load_dotenv('.env')

# firebaseConfig = eval(os.getenv('CONFIG'))

# # Check internet access

# async def connect(host='http://google.com'):
#     try:
#         urllib.request.urlopen(host)

#         # Firebase configuration

#         global firebase
#         firebase = pyrebase.initialize_app(firebaseConfig)
#         global database
#         database = firebase.database()
#         global storage
#         storage = firebase.storage()
#         global auth
#         auth = firebase.auth()

#         return True
#     except:
#         return False

# connect()

# user = {}

# # Colour codes

# PRIMARY = '#8AB1D0'
# SECONDARY = '#0D1931'
# TERTIARY = '#8D887C'
# ACCENT = '#DD4055'
# BG = '#F2EFE9'
# TEXT = '#2E2F2F'

# # Main app class

# async def main(page: flet.Page):

#     # Page Configuration

#     print(page.views,"\n\n\n")
#     page.title = "Unolingo"
#     page.theme_mode = "light"
#     page.window_width = 1440
#     page.window_min_width = 1040
#     page.window_height = 800
#     page.window_min_height = 650
#     page.window_resizable = True
#     page.vertical_alignment = flet.MainAxisAlignment.CENTER
#     page.horizontal_alignment = flet.MainAxisAlignment.CENTER
#     await page.update_async()

#     # User

#     page.session.set('user', {'displayName':'Hi'})
#     await page.update_async()

#     # async def declareUser(email_address: str):
#     #     try:
#     #         user_info = database.child('users').order_by_child('email').equal_to(email_address).get().val()
#     #         global user
#     #         user = dict([*user_info.values()][0])
#     #         global uid
#     #         uid = user['localId']
#     #         global username
#     #         username = user['displayName']
#     #         global email
#     #         email = email_address
#     #         global motherTongue
#     #         motherTongue = database.child(f'users/{uid}/motherTongue').get().val()
#     #         global level
#     #         level = database.child(f'users/{uid}/level').get().val()
#     #     except:
#     #         ...

#     # declareUser('')

#     # Methods

#     async def route_change(e: flet.RouteChangeEvent):
#         page.views.clear()

#         await checkICStatus()
#         await page.update_async()
#         page.views.append(authenticationView)

#         if page.route == '/home':
#             await checkICStatus()
#             await page.update_async()
#             page.session.get('user')
#             await page.views.append(homeView)
        
#         if page.route == '/tutorial':
#             await checkICStatus()
#             await page.update_async()
#             page.session.get('user')
#             await page.views.append(tutorialView)

#         if page.route == '/quiz':
#             await checkICStatus()
#             await page.update_async()
#             page.session.get('user')
#             await page.views.append(quizView)

#         if page.route == '/test':
#             await checkICStatus()
#             await page.update_async()
#             page.session.get('user')
#             await page.views.append(testView)

#         if page.route == '/settings':
#             await checkICStatus()
#             await page.update_async()
#             page.session.get('user')
#             await page.views.append(testView)

#         await page.update_async()
    
#     async def view_pop(e: flet.ViewPopEvent) -> None:
#         page.views.pop()
#         top_view: flet.View = page.views[-1]
#         await page.go_async(top_view.route)
#         await page.update_async()

#     async def checkICStatus():
#         page.banner = ICBanner
#         await page.update_async()
#         if await connect():
#             page.banner.open = False
#             await page.update_async()
#         else:
#             page.banner.open = True
#             await page.update_async()

#     # Sign In
    
#     async def signIn(e: flet.ControlEvent):
#         await checkICStatus()
#         try:
            
#             user_info = auth.sign_in_with_email_and_password(emailSignIn.value, passSignIn.value)
#             # user_info = database.child('users').child(user_info['localId'])
#             # auth.current_user = user_info
#             # page.session.set('user', user_info)
#             # global user
#             # user = page.session.get('user')
#             homeBar.title = flet.Text(user_info)
#             await homeBar.update_async()
#             await page.update_async()
#             await page.go_async('/home')
#             emailSignIn.value, passSignIn.value = None, None
#             emailSignIn.error_text, passSignIn.error_text = '', '123'
#             await page.update_async()
#         except:
#             await checkICStatus()
#             page.show_dialog(signInErrorDialog)
#             await page.update_async()

#     async def clearSignIn(e: flet.ControlEvent):
#         emailSignIn.value, passSignIn.value = None, None
#         await page.update_async()

#     async def signInToSignUp(e: flet.ControlEvent):
#         page.close_dialog()
#         authTabs.selected_index = 1
#         await page.update_async()

#     async def signInError(e: flet.ControlEvent):
#         try:
#             account = database.child('users').order_by_child('email').equal_to(emailSignIn.value).get().val()
#             passSignIn.value = None
#             emailSignIn.error_text = "Incorrect password"
#             await page.update_async()
#         except:
#             emailSignIn.error_text = "Account not found. Sign up instead?"
#             emailSignIn.value, passSignIn.value = None, None
#             await page.update_async()

#     async def validSignInEmail(e: flet.ControlEvent):
#         pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#         if re.match(pattern, emailSignIn.value):
#             emailSignIn.error_text = ""
#             passSignIn.focus()
#             await page.update_async()
#         else:
#             emailSignIn.error_text = "Enter a valid email address"
#             await page.update_async()
    
#     async def is_validSignInEmail():
#         pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#         await page.update_async()
#         return re.match(pattern, emailSignIn.value)

#     async def validSignInPassword(e: flet.ControlEvent):
#         if len(passSignIn.value)>7:
#             passSignIn.error_text = ""
#             await page.update_async()
            
#         else:
#             passSignIn.error_text = "Password must be at least 8 characters long"
#             await page.update_async()

#     async def is_validSignInPassword():
#         await page.update_async()
#         return len(passSignIn.value)>7

#     async def validate_signIn(e: flet.ControlEvent):
#         if all([emailSignIn.value, passSignIn.value, is_validSignInEmail(), is_validSignInPassword()]):
#             signInButton.disabled = False
#         else:
#             signInButton.disabled=True
        
#         await page.update_async()

#     # Sign Up
    
#     async def signUp(e: flet.ControlEvent):
#         await checkICStatus()
#         await page.update_async()
#         try:
#             global user
#             user = auth.create_user_with_email_and_password(emailSignUp.value,passSignUp.value)
#             user['displayName'] = user['email'][:(user['email'].find('@'))]
#             user = database.child(f"users/{user['localId']}").set(user)
#             auth.current_user = user
#             page.session.set('user', user)
#             await page.update_async()
#             print(page.session.get('user'))
#             await page.go_async('/tutorial')
#             emailSignUp.value, passSignUp.value, mtSelection.value, levelSelection.value, tcCheckbox.value = None, None, None, None, None
#             emailSignUp.error_text = ''
#             passSignUp.error_text = ''
#             await page.update_async()
#         except:
#             page.show_dialog(signUpErrorDialog)
#             await page.update_async()

#     async def clearSignUp(e: flet.ControlEvent):
#         emailSignUp.value, passSignUp.value, mtSelection.value, levelSelection.value, tcCheckbox.value = None, None, None, None, None
#         await page.update_async()

#     async def signUpToSignIn(e: flet.ControlEvent):
#         page.close_dialog()
#         authTabs.selected_index = 0
#         await page.update_async()
    
#     async def signUpError(e: flet.ControlEvent):
#         try:
#             account = database.child('users').order_by_child('email').equal_to(emailSignUp.value).get().val()
#             print('GOT A')
#             emailSignUp.value, passSignUp.value, mtSelection.value, levelSelection.value, tcCheckbox.value = None, None, None, None, None
#             emailSignUp.error_text = "Account already exists. Sign in instead."
#             await page.update_async()
#         except:
#             await checkICStatus()
#             emailSignUp.error_text = "Enter a valid email address"
#             emailSignUp.value, passSignUp.value = None, None
#             await page.update_async()

#     async def validSignUpEmail(e: flet.ControlEvent):
#         pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#         if re.match(pattern, emailSignUp.value):
#             emailSignUp.error_text = ""
#             passSignUp.focus()
#             await page.update_async()
#         else:
#             emailSignUp.error_text = "Enter a valid email address"
#             await page.update_async()
    
#     async def is_validSignUpEmail():
#         pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#         await page.update_async()
#         return re.match(pattern, emailSignUp.value)

#     async def validSignUpPassword(e: flet.ControlEvent):
#         if len(passSignUp.value)>7:
#             passSignUp.error_text = ""
#             await page.update_async()
            
#         else:
#             passSignUp.error_text = "Password must be at least 8 characters long"
#             await page.update_async()

#     async def is_validSignUpPassword():
#         await page.update_async()
#         return len(passSignUp.value)>7

#     async def validate_signUp(e: flet.ControlEvent):
#         if all([emailSignUp.value, passSignUp.value, mtSelection.value, levelSelection.value, tcCheckbox.value, is_validSignUpEmail(), is_validSignUpPassword()]):
#             signUpButton.disabled = False
#             await page.update_async()
#         else:
#             signUpButton.disabled=True
#             await page.update_async()
        
#         await page.update_async()

#     # async def showConfirmSignUpDialog(e: flet.ControlEvent):
#     #     global mother_tongue
#     #     mother_tongue = mtSelection.value
#     #     global level
#     #     level = levelSelection.value
#     #     await mtSelection.update_async()
#     #     await levelSelection.update_async()
#     #     page.show_dialog(confirmSignUpDialog)

#     async def logout(e: flet.ControlEvent):
#         auth.current_user = None
#         page.session.clear()
#         await page.go_async('/authentication')
#         authTabs.selected_index=0
#         emailSignIn.focus()
#         await page.update_async()

#     # UI Elements

#     ICBanner = flet.Banner(
#         bgcolor=flet.colors.AMBER_100,
#         leading=flet.Icon(flet.icons.WARNING_AMBER_ROUNDED, color=flet.colors.AMBER, size=40),
#         content=flet.Text(
#             "Oops, it seems like you are not connected to the internet.",
#         ),
#         actions=[
#             flet.TextButton("Retry", on_click=checkICStatus),
#             flet.TextButton("Quit", on_click=lambda _ : page.window_close()),
#         ],
#     )

#     await checkICStatus()

#     imageColumn = flet.Column(
#         controls = [
#             flet.Image(
#                 src='https://img.freepik.com/free-photo/painting-mountain-lake-with-mountain-background_188544-9126.jpg',
#                 opacity=0.9,
#                 fit=flet.ImageFit.COVER,
#                 expand=True
#             )
#         ],
#         expand=True
#     )

#     # Sign In

#     signInErrorDialog = flet.AlertDialog(
#         modal=True,
#         title=flet.Text("Invalid credentials", style=flet.TextThemeStyle.LABEL_LARGE, size=20),
#         content=flet.Text("Please try again or Sign up."),
#         actions=[
#             flet.ElevatedButton("Retry", on_click=lambda _ : page.close_dialog()),
#             flet.ElevatedButton("Sign Up", on_click=signInToSignUp),
#         ],
#         actions_alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
#         on_dismiss=signInError,
            
#     )

#     emailSignIn=flet.TextField(
#         label='Email address',
#         icon=flet.icons.MAIL,
#         color=TEXT,
#         border_color=SECONDARY,
#         cursor_color=SECONDARY,
#         focused_border_color=SECONDARY,
#         focused_color=SECONDARY,
#         keyboard_type='email',
#         autocorrect=False,
#         dense=True,
#         on_submit=validSignInEmail,
#         on_change=validate_signIn
#     )

#     passSignIn=flet.TextField(
#         label='Password',
#         icon=flet.icons.LOCK,
#         color=TEXT,
#         border_color=SECONDARY,
#         cursor_color=SECONDARY,
#         focused_border_color=SECONDARY,
#         focused_color=SECONDARY,
#         keyboard_type='password',
#         autocorrect=False,
#         dense=True,
#         password=True,
#         can_reveal_password=True,
#         on_change=validate_signIn,
#         on_submit=validSignInPassword,
#         error_text=""
#     )

#     signInButton=flet.ElevatedButton(
#         text="Sign in",
#         color=SECONDARY,
#         bgcolor=PRIMARY,
#         height=40,
#         disabled = True,
#         expand=True,
#         on_click=signIn,
#     )

#     clearSignInButton=flet.IconButton(
#         icon=flet.icons.CLOSE_ROUNDED,
#         style=flet.ButtonStyle(
#             bgcolor=flet.colors.BLUE_200,
#             shape={
#                 flet.MaterialState.HOVERED: flet.RoundedRectangleBorder(radius=10),
#                 flet.MaterialState. DEFAULT: flet.RoundedRectangleBorder(radius=50),
#             },
#         ),
#         on_click=clearSignIn,
#         tooltip="Clear section"
#     )

#     # Sign Up

#     signUpErrorDialog = flet.AlertDialog(
#         modal=True,
#         title=flet.Text("Error encountered when creating account", style=flet.TextThemeStyle.LABEL_LARGE, size=20),
#         content=flet.Text("Please try again or Sign in."),
#         actions=[
#             flet.ElevatedButton("Retry", on_click=lambda _ : page.close_dialog()),
#             flet.ElevatedButton("Sign In", on_click=signUpToSignIn),
#         ],
#         actions_alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
#         on_dismiss=signUpError,
            
#     )

#     emailSignUp=flet.TextField(
#         label='Email address',
#         icon=flet.icons.MAIL,
#         color=TEXT,
#         border_color=SECONDARY,
#         cursor_color=SECONDARY,
#         focused_border_color=SECONDARY,
#         focused_color=SECONDARY,
#         keyboard_type='email',
#         autocorrect=False,
#         dense=True,
#         on_submit=validSignUpEmail,
#         on_change=validate_signUp
#     )

#     passSignUp=flet.TextField(
#         label='Password',
#         icon=flet.icons.LOCK,
#         color=TEXT,
#         border_color=SECONDARY,
#         cursor_color=SECONDARY,
#         focused_border_color=SECONDARY,
#         focused_color=SECONDARY,
#         keyboard_type='password',
#         autocorrect=False,
#         dense=True,
#         password=True,
#         can_reveal_password=True,
#         on_change=validate_signUp,
#         on_submit=validSignUpPassword,
#         error_text=""
#     )

#     mtSelection = flet.Dropdown(
#         label="Mother-tongue language",
#         options=[
#             flet.dropdown.Option('Chinese'),
#         ],
#         dense=True,
#         icon=flet.icons.LANGUAGE,
#         color=TEXT,
#         text_size=17,
#         border_color=SECONDARY,
#         focused_border_color=SECONDARY,
#         focused_color=SECONDARY,
#         on_change=validate_signUp,
#         expand=True
#     )

#     levelSelection = flet.Dropdown(
#         label="Level",
#         options=[
#             flet.dropdown.Option('1'),
#             flet.dropdown.Option('2'),
#             flet.dropdown.Option('3'),
#             flet.dropdown.Option('4'),
#             flet.dropdown.Option('5'),
#             flet.dropdown.Option('6'),
#         ],
#         dense=True,
#         color=TEXT,
#         text_size=17,
#         border_color=SECONDARY,
#         focused_border_color=SECONDARY,
#         focused_color=SECONDARY,
#         expand=True,
#         prefix=flet.Text('Primary '),
#         on_change=validate_signUp,
#     )

#     tcCheckbox = flet.Checkbox(
#         label="By signing up for an account, I agree to the Terms and Conditions",
#         label_position='right',
#         fill_color=TERTIARY,
#         on_change=validate_signUp,
#         expand=True
#     )

#     # confirmSignUpDialog = flet.AlertDialog(
#     #     modal=True,
#     #     title=flet.Text("Do you confirm the following:", style=flet.TextThemeStyle.LABEL_LARGE, size=20),
#     #     content=flet.Text(f"Primary {level} {mother_tongue}\nThis information cannot be changed."),
#     #     actions=[
#     #         flet.ElevatedButton("Edit", on_click=lambda _ : page.close_dialog()),
#     #         flet.ElevatedButton("Confirm", on_click=signUp, elevation=2, bgcolor=ACCENT),
#     #     ],
#     #     actions_alignment=flet.MainAxisAlignment.END,
#     #     on_dismiss=lambda _ : levelSelection.focus(),
            
#     # )

#     signUpButton=flet.ElevatedButton(
#         text="Sign up",
#         color=SECONDARY,
#         bgcolor=PRIMARY,
#         height=40,
#         disabled = True,
#         expand=True,
#         on_click=signUp,
#     )

#     clearSignUpButton=flet.IconButton(
#         icon=flet.icons.CLOSE_ROUNDED,
#         style=flet.ButtonStyle(
#             bgcolor=flet.colors.BLUE_200,
#             shape={
#                 flet.MaterialState.HOVERED: flet.RoundedRectangleBorder(radius=10),
#                 flet.MaterialState.DEFAULT: flet.RoundedRectangleBorder(radius=50),
#             },
#         ),
#         on_click=clearSignUp,
#         tooltip="Clear section",
#     )

#     await checkICStatus()
#     await page.update_async()
#     user = page.session.get('user')

#     # Authentication View

#     authenticationView = flet.View(
#         route = '/authentication',
#         controls = [
#             flet.Row(
#                 controls = [
#                     imageColumn,

#                     flet.VerticalDivider(
#                         color=TERTIARY,
#                         thickness = 3,
#                         width = 8,
#                     ),

#                     flet.Column(
#                         controls = [
#                             flet.Container(
#                                 content=(authTabs:=flet.Tabs(
#                                     tabs = [
#                                         flet.Tab(
#                                             text="Sign In",
#                                             content=flet.Container(
#                                                 content=flet.Column(
#                                                     controls=[
#                                                         flet.Column(
#                                                             controls=[
#                                                                 flet.Text(value='Welcome back!', size=34,color=SECONDARY, weight='w700'),
#                                                                 flet.Text(value='Log in to your account', size=20,color=TEXT, weight='w300')
#                                                             ],
#                                                             spacing=-50,
#                                                         ),
                                                        
#                                                         flet.Container(
#                                                             content=flet.Icon(name='lock_person',size=200, color=TERTIARY),
#                                                             alignment=flet.alignment.center,
#                                                         ),

#                                                         flet.Column(
#                                                             controls=[
#                                                                 emailSignIn,

#                                                                 passSignIn,

#                                                                 flet.Container(
#                                                                     content=flet.Row(
#                                                                         controls=[
#                                                                             clearSignInButton,
#                                                                             signInButton
#                                                                         ]
#                                                                     ),
#                                                                     alignment=flet.alignment.center,
#                                                                 ),
#                                                             ],
#                                                             expand=True,
#                                                             spacing=20,
#                                                             alignment=flet.CrossAxisAlignment.CENTER
#                                                         ),
                                                        
#                                                     ],
#                                                     expand=True,
#                                                     spacing=30,
#                                                     alignment=flet.MainAxisAlignment.CENTER,
#                                                     horizontal_alignment=flet.MainAxisAlignment.END
#                                                 ),
#                                                 padding=20,
#                                                 expand=True
#                                             ),
#                                         ),
#                                         flet.Tab(
#                                             text="Sign Up",
#                                             content=flet.Container(
#                                                 content=flet.Column(
#                                                     controls=[
#                                                         flet.Column(
#                                                             controls=[
#                                                                 flet.Text(value='Welcome!', size=34,color=SECONDARY, weight='w700'),
#                                                                 flet.Text(value="Let's create your account", size=20,color=TEXT, weight='w300')
#                                                             ],
#                                                             spacing=-50,
#                                                         ),
                                                        
#                                                         flet.Container(
#                                                             content=flet.Icon(name='person',size=100,color=TERTIARY),
#                                                             alignment=flet.alignment.center,
#                                                         ),

#                                                         flet.Column(
#                                                             controls=[
#                                                                 emailSignUp,

#                                                                 passSignUp,

#                                                                 flet.Row(
#                                                                     controls=[
#                                                                         mtSelection,
#                                                                         levelSelection,
#                                                                     ],
#                                                                     alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
#                                                                     spacing=10
#                                                                 ),
                                                                
#                                                             ],
#                                                             expand=True,
#                                                             spacing=15,
#                                                             alignment=flet.CrossAxisAlignment.CENTER
#                                                         ),

#                                                         flet.Column(
#                                                             controls=[
#                                                                 tcCheckbox,

#                                                                 flet.Container(
#                                                                     content=flet.Row(
#                                                                         controls=[
#                                                                             clearSignUpButton,
#                                                                             signUpButton
#                                                                         ]
#                                                                     ),
#                                                                     alignment=flet.alignment.center,
#                                                                 ),
#                                                             ],
#                                                             expand=True,
#                                                             alignment=flet.MainAxisAlignment.CENTER
#                                                         ),
                                                        
#                                                     ],
#                                                     expand=True,
#                                                     spacing=25,
#                                                     alignment=flet.MainAxisAlignment.CENTER,
#                                                     horizontal_alignment=flet.MainAxisAlignment.END
#                                                 ),
#                                                 padding=20,
#                                                 expand=True
#                                             ),
#                                         ),
#                                     ],
#                                     animation_duration = 300,
#                                     width = (page.window_width/2) - 30,
#                                     height = page.window_height,
#                                     scrollable=True,
#                                     expand=True,
#                                 )),
#                                 expand=True,
#                                 alignment=flet.alignment.center
#                             )
                            
#                         ],
#                         alignment=flet.MainAxisAlignment.CENTER,
#                         horizontal_alignment=flet.MainAxisAlignment.CENTER,
#                         expand=True
#                     ),
#                 ],
#                 width = page.window_width,
#                 height = page.window_height,
#                 vertical_alignment = flet.CrossAxisAlignment.START,
#                 spacing=0,
#                 alignment = flet.MainAxisAlignment.START,
#                 expand=True
#             )
#         ],
#         bgcolor = BG,
#         padding = 0
#     )

#     # Tutorial View
    
#     tutorialView = flet.View(
#         route='/tutorial',
#         controls=[
#             flet.AppBar(
#                 leading=flet.Icon(flet.icons.HELP),
#                 leading_width=40,
#                 title=flet.Text(page.session.get('user')['displayName']),
#                 center_title=False,
#                 bgcolor=flet.colors.SURFACE_VARIANT,
#                 actions=[
#                     flet.IconButton(flet.icons.WB_SUNNY_OUTLINED),
#                     flet.IconButton(flet.icons.FILTER_3,on_click=logout),
#                     flet.PopupMenuButton(
#                         items=[
#                             flet.PopupMenuItem(text="Item 1"),
#                             flet.PopupMenuItem(),  # divider
#                             flet.PopupMenuItem(
#                                 text="Checked item", checked=False, on_click=lambda _ : print('clicked')
#                             ),
#                         ]
#                     ),
#                 ],
#             )
#         ]
#     )

#     # Home View
    
#     homeView = flet.View(
#         route='/home',
#         controls=[
#             homeBar:=flet.AppBar(
#                 leading=flet.Icon(flet.icons.HOUSE),
#                 leading_width=40,
#                 title=flet.Text(None),
#                 center_title=False,
#                 bgcolor=flet.colors.SURFACE_VARIANT,
#                 actions=[
#                     flet.IconButton(flet.icons.WB_SUNNY_OUTLINED),
#                     flet.IconButton(
#                         flet.icons.FILTER_3,
#                         on_click=logout
#                     ),
#                     flet.PopupMenuButton(
#                         items=[
#                             flet.PopupMenuItem(text="Item 1"),
#                             flet.PopupMenuItem(),  # divider
#                             flet.PopupMenuItem(
#                                 text="Checked item", checked=False, on_click=lambda _ : print('clicked')
#                             ),
#                         ]
#                     ),
#                 ],
#             )
#         ]
#     )

#     # Quiz View
    
#     quizView = flet.View(
#         route='/quiz'
#     )

#     # Test View
    
#     testView = flet.View(
#         route='/test'
#     )

#     # Settings View
    
#     settingsView = flet.View(
#         route='/settings'
#     )

#     page.on_route_change = route_change
#     page.on_view_pop = view_pop
#     await checkICStatus()
#     await page.go_async(page.route)


# if __name__  ==  "__main__":
#     flet.app(target = main, view = flet.FLET_APP)