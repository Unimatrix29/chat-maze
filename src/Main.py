import random
import keyboard
from Screen import Screen 
from MazeGenerator import MazeGenerator
import Player
from Controller import Controller

running = False

main_screen = Screen()
maze_generator = MazeGenerator()
controller = Controller()
#program start
running = True

main_screen.setup_screen()
main_screen.update_screen(maze_generator.random_maze(), [5, 7])
#while running:
while True:
    pass

    
    
    




