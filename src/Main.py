from Screen import Screen
from MazeGenerator import MazeGenerator

window = Screen()
mazeGenerator = MazeGenerator()

window.setup_screen()
maze = mazeGenerator.get_preset("maze_1")

while True:
    window.update_screen(maze, [4, 2])