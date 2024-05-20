from Screen import Screen 

class Player:
    def __init__(self, maze):
        self.activeMaze = maze

        self.currentPosition = maze[1]

    def UpdateMaze(self, newMaze):
        pass

    def move(self, mVector):
        self.currentPosition[0] += mVector[0]
        self.currentPosition[1] += mVector[1]
    """
    Sets currentPosition to a point
    """
    def set_position(self, point):
        self.currentPosition[0] = point[0]
        self.currentPosition[1] = point[1]
    
