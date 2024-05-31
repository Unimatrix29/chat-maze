from Screen import Screen
import pygame
from MazeGenerator import MazeGenerator
from Player import Player

textWindow = Screen()
player = Player(MazeGenerator.get_preset(MazeGenerator))

textWindow.setup_screen()

while True:
    textWindow.update_screen(MazeGenerator.get_preset(), player)
    if(textWindow.on_return()):
        print(textWindow.get_user_input())
    