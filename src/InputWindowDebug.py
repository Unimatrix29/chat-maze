from Controller import Controller
import pygame

textWindow = Controller()

textWindow.setup_screen()

while True:
    textWindow.update_screen()
    if(textWindow.on_return()):
        print(textWindow.get_user_input())
    