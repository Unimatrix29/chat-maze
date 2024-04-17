import Screen 

class Palyer:
    def __init__(self, maze):
        self.activeMaze = maze

        #dependent on the actual implementation of the maze 
        self.currentPosition = maze[1]

        #added a variable to hold and initiate a screen obj 
        self.__screen = Screen()