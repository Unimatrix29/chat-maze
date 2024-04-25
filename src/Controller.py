import random 
import tkinter as tk

class Controller():

    def __init__(self):
        self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "deny": [0, 0]}
        self.root = tk.Tk()
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.submit_button = tk.Button(self.root, text = "Submit", command = self.console_input)
        self.submit_button.pack()
        

    

    def console_input(self):
        direction_request = self.entry.get()
        if direction_request.strip().lower() in self.move_options:
            return self.move_options[direction_request]
        else:
            return self.move_options["deny"]
        
