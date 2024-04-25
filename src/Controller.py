import random 

class Controller():

    def __init__(self):
        self.move_options = ["deny", "up", "down", "left", "right"]

    def console_input(self):
        self.direction_request = input("Type a direction: ")
        if self.direction_request.strip().lower() in self.move_options:
            return self.direction_request
        else:
            return self.move_options[0]
        