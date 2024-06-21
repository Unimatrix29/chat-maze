"""
Player class represents a chatGPT
character on a playfield
"""
class Player:
    def __init__(self, maze, name = ""):
        self.currentPosition = [int(maze[1][0]), int(maze[1][1])]
        self.name = name
        self.isHidden = False
    """
    Changes currentPosition by a move vector
    """
    def move(self, mVector):
        self.currentPosition[0] += mVector[0]
        self.currentPosition[1] += mVector[1]
    """
    Sets currentPosition to a point
    """
    def set_position(self, point):
        self.currentPosition[0] = point[0]
        self.currentPosition[1] = point[1]
    """
    Returns currentPosition after rotating it by [count] times
    """
    def get_rotated_position(self, count = 1):
        rotatedPosition = [self.currentPosition[0], self.currentPosition[1]]
        for i in range(count):
            rotatedPosition = [rotatedPosition[1], 15 - rotatedPosition[0]]
            
        return rotatedPosition
    """
    Changes render visibility
    """
    def hide(self, request: bool):
        self.isHidden = request
    """
    Changes player's name
    (by switching prompts)
    """
    def change_name(self, newName: str):
        self.name = newName