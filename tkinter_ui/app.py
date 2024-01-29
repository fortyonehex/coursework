import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Change Frames")
        self.set_aspect(480, 360)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.cframe = Setup(self.container, self)
        self.cframe.grid(row=0, column=0, sticky="nsew")
        self.frame = self.cframe
        self.tkraise()
    
    def set_aspect(self, width, height):
        self.scale = width/480
        self.minsize(width=width, height=height)
        self.maxsize(width=width, height=height)

class Setup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        ttk.Style().configure("TButton", font=("System", int(14*controller.scale)))

        label = ttk.Label(self, text="penis", font=("System", int(24*controller.scale)))
        label.pack(padx=int(20*controller.scale), pady=int(20*controller.scale))

        button = ttk.Button(self, text="480x360", command=lambda: self.reinit(controller, 480, 360))
        button.pack()
        button2 = ttk.Button(self, text="640x480", command=lambda: self.reinit(controller, 640, 480))
        button2.pack()
        button3 = ttk.Button(self, text="800x600", command=lambda: self.reinit(controller, 800, 600))
        button3.pack()
        button4 = ttk.Button(self, text="960x720", command=lambda: self.reinit(controller, 960, 720))
        button4.pack()

    def reinit(self, controller, w, h):
        controller.set_aspect(w, h)
        controller.cframe = Setup(controller.container, controller)
        controller.cframe.grid(row=0, column=0, sticky="nsew")
        controller.frame = controller.cframe
        controller.tkraise()