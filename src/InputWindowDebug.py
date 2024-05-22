from Controller import Controller
import pygame

textWindow = Controller()

textWindow.setup_input_window()

for event in pygame.event.get():
    if event.type == pygame.QUIT:
            textWindow.quit_screen()
    
    textWindow.update_screen()