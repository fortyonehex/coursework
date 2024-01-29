import customtkinter
from app import App

"""customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("960x720")

def button_function():
    print("button pressed")

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

app.mainloop()"""

main_app = App()
main_app.mainloop()