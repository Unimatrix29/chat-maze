import pygame
from Screen import Screen
from MazeGenerator import MazeGenerator
from Player import Player
from Controller import Controller

window = Screen()
mazeGenerator = MazeGenerator()
player = Player()

window.setup_screen()
maze = mazeGenerator.get_preset("maze_1")
player.move(maze[1]) # The structure of mazes is unclear(?)

while True:
    
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            mVector = Controller.get_movement(event.key)    #Note: Probably add a list of moveKeys
            player.move(mVector)                            #      to avoid unnecessary 0-movements
                
        if event.type == pygame.QUIT:
            window.quit_screen()

    window.update_screen(maze, player.currentPosition)