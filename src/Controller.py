import random 
import pygame

class Controller():

    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

    def setup_input_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode([700, 700])
        pygame.display.set_caption("text_input")
        self.font = pygame.font.Font(None, 64)
        self.text = ""

    def update_screen(self):
        self.screen.fill(self.BLACK)
        self.text_surface = self.font.render(self.text, True, self.WHITE)

        pygame.display.flip()





    def console_input(self):
        direction_request = input("Type a direction: ")
        if direction_request.strip().lower() in self.move_options:
            return self.move_options[direction_request]
        else:
            return self.move_options["deny"]
        
    


    



        
