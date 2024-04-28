import pygame
from Screen import Screen
from MazeGenerator import MazeGenerator
from Player import Player
from Controller import Controller

window = Screen()
mazeGenerator = MazeGenerator()
player = Player()

gameOver = False

window.setup_screen()
maze = mazeGenerator.get_preset("maze_1")
player.move(maze[1])

while True:
    
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            # Game restart by pressing R key
            if event.key == pygame.K_r:
                gameOver = False
                maze = mazeGenerator.get_preset("maze_1")
                player.set_position(maze[1])

            if not gameOver:
                mVector = Controller.get_movement(event.key)    #Note: Probably add a list of moveKeys
                player.move(mVector)                            #      to avoid unnecessary 0-movements
                
        if event.type == pygame.QUIT:
            window.quit_screen()

    if window.check_wall(maze, player.currentPosition):
        # Changing actual maze to an end screen (sad)
        maze = mazeGenerator.get_preset("LOST")
        player.set_position([-1, -1])
        gameOver = True
    if window.check_finish(maze, player.currentPosition):
        # Changing actual maze to an end screen (happy)
        maze = mazeGenerator.get_preset("FINISH")
        player.set_position([-1, -1])
        gameOver = True
        
    
    window.update_screen(maze, player.currentPosition)