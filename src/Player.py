from Screen import Screen 

class Player:
    def __init__(self, maze, screen):
        self.activeMaze = maze

        self.currentPosition = maze[1]
        
        self.__screen = screen

    def UpdateMaze(self, newMaze):
        pass

    def MoveUp(self):
        self.newPosition = self.currentPosition
        self.newPosition[1] = self.currentPosition[1] - 1

        if not self.__screen.check_wall(self.activeMaze, self.newPosition):
            self.currentPosition = self.newPosition

    def MoveDown(self):
        self.newPosition = self.currentPosition
        self.newPosition[1] = self.currentPosition[1] + 1

        if not self.__screen.check_wall(self.activeMaze, self.newPosition):
            self.currentPosition = self.newPosition

    def MoveLeft(self):
        self.newPosition = self.currentPosition 
        self.newPosition[0] = self.currentPosition[0] - 1

        if not self.__screen.check_wall(self.activeMaze, self.newPosition):
            self.currentPosition = self.newPosition

    def MoveRight(self):
        self.newPosition = self.currentPosition
        self.newPosition[0] = self.currentPosition[0] + 1

        if not self.__screen.check_wall(self.activeMaze, self.newPosition):
            self.currentPosition = self.newPosition