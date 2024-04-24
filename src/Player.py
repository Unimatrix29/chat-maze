#Note: !This is a test implementation!
class Player:
    
    def __init__(self, x = 0, y = 0):
        self.currentPosition = [x, y]
        
    """
    Adds a moving vector to current position
    """
    def move(self, mVector):
        self.currentPosition[0] += mVector[0]
        self.currentPosition[1] += mVector[1]