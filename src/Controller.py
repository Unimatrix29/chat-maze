import random 
import tkinter as tk
from tkinter import ttk

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
        window = tk.Tk()
        window.geometry("500x100")
        window.title("PROMPT INPUT")
        submit_button = ttk.Button(window, text = "send prompt to ChatGPT")
        submit_button.pack(expand = True)
        
