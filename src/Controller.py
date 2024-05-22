import random 
import pygame

class Controller():

    def __init__(self):
        self.setup_input_window()

    def setup_input_window(self):
        global screen
        pygame.init()
        screen = pygame.display.set_mode([700, 700])
        pygame.display.set_caption("text_input")
        screen.fill(0,0,0)

    def update_screen(self, maze, player_pos):
        

        pygame.display.flip()





    def console_input(self):
        direction_request = input("Type a direction: ")
        if direction_request.strip().lower() in self.move_options:
            return self.move_options[direction_request]
        else:
            return self.move_options["deny"]
        
    


    



        
