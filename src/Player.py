from Screen import Screen 

class Player:
    def __init__(self, maze, screen):
        #assuming that acivteMaze is a 3D array and the actual representation of the maze is at index 0, 
        #the start position at index 1 and the end position at index 2
        self.activeMaze = maze

        #dependent on the actual implementation of the maze 
        self.currentPosition = maze[1]

        #added a variable to hold and initiate a screen obj 
        self.__screen = screen

    def UpdateMaze(self, newMaze):
        pass