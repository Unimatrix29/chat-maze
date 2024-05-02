import random 
import tkinter as tk
from tkinter import ttk
from tkinter import *

class Controller():

    def __init__(self):
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}

    def console_input(self):
        direction_request = input("Type a direction: ")
        if direction_request.strip().lower() in self.move_options:
            return self.move_options[direction_request]
        else:
            return self.move_options["deny"]
        
    def setup_prompt_window(self):
        #setup input window
        self.window = tk.Tk()
        self.window.geometry("500x100")
        self.window.title("PROMPT INPUT")

        
    
        
    def init_prompt_window(self):

        #setup prompt input field
        e = Entry(self.window, width = 50, bg = "lightgreen", borderwidth = 5)
        e.pack()

        def submit_text():
            mylabel = Label(self.window, text = e.get())
            mylabel.pack()
            e.delete(0, 'end')

        #setup submit button
        submit_button = ttk.Button(self.window, text = "send prompt to ChatGPT", command = submit_text)
        submit_button.pack(expand = True)

        self.window.mainloop()

    



        
