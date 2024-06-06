class Player:
    def __init__(self, maze):
        self.currentPosition = [int(maze[1][0]), int(maze[1][1])]
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
            rotatedPosition = [self.currentPosition[1], 15 - self.currentPosition[0]]
            
        return rotatedPosition
    """
    Changes render visibility
    """
    def hide(self, request: bool):
        self.isHidden = request
